# doc_translator.py
import html
import io
import os
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import fitz  # pymupdf

from server import translate_text


def extract_blocks_with_lines(page) -> List[Dict]:
    """
    Returns a list of blocks, each with lines -> spans and their bboxes and the block bbox.
    Each block: { 'bbox':(x0,y0,x1,y1), 'lines': [ { 'bbox':(x0,y0,x1,y1), 'text': '...', 'spans':[ {...} ] } ] }
    """
    blocks = []
    d = page.get_text("dict")
    for b in d.get("blocks", []):
        if "lines" not in b or not b["lines"]:
            continue
        block_bbox = tuple(b["bbox"])
        lines_out = []
        avg_font_size = 0
        font_sizes = []

        for line in b["lines"]:
            # compute line bbox from spans
            spans = []
            line_text_parts = []
            lx0, ly0, lx1, ly1 = None, None, None, None
            for span in line.get("spans", []):
                s_text = span.get("text", "")
                if not s_text:
                    continue
                sx0, sy0, sx1, sy1 = span.get("bbox", [0, 0, 0, 0])
                spans.append(
                    {
                        "text": s_text,
                        "bbox": (sx0, sy0, sx1, sy1),
                        "size": span.get("size"),
                    }
                )
                line_text_parts.append(s_text)
                if span.get("size"):
                    try:
                        font_sizes.append(float(span.get("size")))
                    except Exception:
                        pass

                if lx0 is None:
                    lx0, ly0, lx1, ly1 = sx0, sy0, sx1, sy1
                else:
                    lx0 = min(lx0, sx0)
                    ly0 = min(ly0, sy0)
                    lx1 = max(lx1, sx1)
                    ly1 = max(ly1, sy1)
            line_text = "".join(line_text_parts).strip()
            if line_text == "":
                continue
            if lx0 is None:
                lx0, ly0, lx1, ly1 = block_bbox
            lines_out.append(
                {"bbox": (lx0, ly0, lx1, ly1), "text": line_text, "spans": spans}
            )

        if not lines_out:
            continue

        # Calculate average font size for the block
        if font_sizes:
            avg_font_size = sum(font_sizes) / len(font_sizes)

        blocks.append(
            {"bbox": block_bbox, "lines": lines_out, "avg_font_size": avg_font_size}
        )
    return blocks


def _try_insert_html_in_rect(page, rect, html_block):
    """
    Attempt insert_htmlbox and return True if it succeeded, False otherwise.
    """
    try:
        page.insert_htmlbox(rect, html_block)
        return True
    except Exception as e:
        return False


def _insert_html_with_shrink(
    page,
    rect,
    text_html,
    fontfile_uri: str = None,
    start_fs: float = 12.0,
    min_fs: float = 6.0,
) -> float:
    """
    Insert html into rect using insert_htmlbox. Try starting fontsize start_fs and shrink until min_fs.
    Returns the fontsize used (or 0 on total failure).
    """
    family = None
    font_face_css = ""
    if fontfile_uri:
        family = "F_" + Path(fontfile_uri).stem.replace("-", "_").replace(".", "_")
        font_face_css = f"@font-face{{font-family:'{family}'; src: url('{fontfile_uri}') format('truetype');}}"
        font_family_css = f"'{family}', sans-serif"
    else:
        font_family_css = "sans-serif"

    fs = start_fs
    attempt = 0
    while fs >= min_fs and attempt < 14:
        attempt += 1
        css = (
            "<style>"
            + font_face_css
            + f"div.trans{{font-family:{font_family_css}; font-size:{fs:.2f}pt; line-height:1.12; white-space:pre-wrap; overflow-wrap:anywhere; word-break:break-word; margin:0; padding:0;}}"
            + "</style>"
        )
        html_block = css + "<div class='trans'>" + text_html + "</div>"
        if _try_insert_html_in_rect(page, rect, html_block):
            return fs
        fs *= 0.85
    return 0.0


def _rect_coords(rect: fitz.Rect) -> Tuple[float, float, float, float]:
    """Return (x0, y0, x1, y1) coordinates from a fitz.Rect."""
    try:
        return float(rect.x0), float(rect.y0), float(rect.x1), float(rect.y1)
    except Exception:
        if hasattr(rect, "tl") and hasattr(rect, "br"):
            tl = rect.tl
            br = rect.br
            return float(tl.x), float(tl.y), float(br.x), float(br.y)
        try:
            t = tuple(rect)
            if len(t) >= 4:
                return float(t[0]), float(t[1]), float(t[2]), float(t[3])
        except Exception:
            pass
    raise RuntimeError("Cannot extract coordinates from Rect-like object")


def _rect_area(rect):
    """Compute area of a fitz.Rect."""
    x0, y0, x1, y1 = _rect_coords(rect)
    return max(0.0, (x1 - x0)) * max(0.0, (y1 - y0))


def _rects_overlap(r1: fitz.Rect, r2: fitz.Rect, margin: float = 2.0) -> bool:
    """
    Check if two rectangles overlap with a margin.
    Returns True if they overlap or are within margin pixels of each other.
    """
    # Expand r2 by margin to create a buffer zone
    expanded_r2 = fitz.Rect(
        r2.x0 - margin, r2.y0 - margin, r2.x1 + margin, r2.y1 + margin
    )

    # Check if r1 intersects with expanded r2
    if (
        r1.x1 <= expanded_r2.x0
        or r1.x0 >= expanded_r2.x1
        or r1.y1 <= expanded_r2.y0
        or r1.y0 >= expanded_r2.y1
    ):
        return False
    return True


def _get_image_bboxes_from_page(page: fitz.Page) -> List[fitz.Rect]:
    """Return a list of image bounding boxes present on the page."""
    rects = []
    try:
        blocks = page.get_text("dict").get("blocks", [])
        for b in blocks:
            if b.get("type") == 1:  # Image block
                rect = fitz.Rect(b["bbox"])
                rects.append(rect)
    except Exception:
        pass
    return rects


def _find_safe_placement_rect(
    original_rect: fitz.Rect,
    occupied_rects: List[fitz.Rect],
    page_rect: fitz.Rect,
    margin: float = 4.0,
) -> Optional[fitz.Rect]:
    """
    Find a safe rectangle for placement that doesn't overlap with occupied areas.
    Try to keep it as close to original position as possible.
    """
    # First, check if original rect is already safe
    safe = True
    for occupied in occupied_rects:
        if _rects_overlap(original_rect, occupied, margin):
            safe = False
            break

    if safe:
        return original_rect

    # Strategy 1: Try shifting down
    for y_offset in range(0, int(page_rect.height - original_rect.y0), 8):
        candidate = fitz.Rect(
            original_rect.x0,
            original_rect.y0 + y_offset,
            original_rect.x1,
            original_rect.y1 + y_offset,
        )

        # Check if candidate is within page bounds
        if candidate.y1 > page_rect.y1 - margin:
            break

        # Check if candidate is safe
        is_safe = True
        for occupied in occupied_rects:
            if _rects_overlap(candidate, occupied, margin):
                is_safe = False
                break

        if is_safe:
            return candidate

    # Strategy 2: Try shifting right
    for x_offset in range(0, int(page_rect.width - original_rect.x0), 8):
        candidate = fitz.Rect(
            original_rect.x0 + x_offset,
            original_rect.y0,
            original_rect.x1 + x_offset,
            original_rect.y1,
        )

        if candidate.x1 > page_rect.x1 - margin:
            break

        is_safe = True
        for occupied in occupied_rects:
            if _rects_overlap(candidate, occupied, margin):
                is_safe = False
                break

        if is_safe:
            return candidate

    # Strategy 3: Find first available space going top to bottom
    step = 20
    for y in range(
        int(page_rect.y0) + int(margin),
        int(page_rect.y1) - int(original_rect.height),
        step,
    ):
        for x in range(
            int(page_rect.x0) + int(margin),
            int(page_rect.x1) - int(original_rect.width),
            step,
        ):
            candidate = fitz.Rect(
                x, y, x + original_rect.width, y + original_rect.height
            )

            if (
                candidate.x1 > page_rect.x1 - margin
                or candidate.y1 > page_rect.y1 - margin
            ):
                continue

            is_safe = True
            for occupied in occupied_rects:
                if _rects_overlap(candidate, occupied, margin):
                    is_safe = False
                    break

            if is_safe:
                return candidate

    # If no safe position found, return None
    return None


def _expand_rect_to_available_space(
    original_rect: fitz.Rect,
    occupied_rects: List[fitz.Rect],
    page_rect: fitz.Rect,
    max_expand_pixels: int = 80,
    step: int = 8,
    margin: float = 4.0,
) -> fitz.Rect:
    """
    Try to expand the original_rect in width and height while staying in free space.
    This helps create room for larger font sizes. Returns the expanded rect (may be same as original if no room).
    """
    best = fitz.Rect(original_rect)
    # try to increase width and height gradually
    for expand in range(step, max_expand_pixels + step, step):
        candidate = fitz.Rect(
            max(page_rect.x0 + margin, original_rect.x0 - expand // 2),
            max(page_rect.y0 + margin, original_rect.y0 - expand // 4),
            min(page_rect.x1 - margin, original_rect.x1 + expand // 2),
            min(page_rect.y1 - margin, original_rect.y1 + expand // 4),
        )
        # ensure candidate is at least as big as original
        if (
            candidate.width < original_rect.width
            or candidate.height < original_rect.height
        ):
            continue

        # check overlap
        conflict = False
        for occupied in occupied_rects:
            if _rects_overlap(candidate, occupied, margin):
                conflict = True
                break
        if not conflict:
            # prefer larger area
            if _rect_area(candidate) > _rect_area(best):
                best = candidate
    return best


def _fontfile_to_file_uri(fontfile: Optional[str]) -> Optional[str]:
    if not fontfile:
        return None
    p = Path(fontfile)
    try:
        p_abs = p.resolve(strict=True)
    except Exception:
        return None
    if not os.access(str(p_abs), os.R_OK):
        return None
    try:
        return p_abs.as_uri()
    except Exception:
        return None


def _copy_font_to_temp_and_get_uri(fontfile: str) -> Optional[str]:
    try:
        data = Path(fontfile).read_bytes()
    except Exception:
        return None
    suffix = Path(fontfile).suffix or ".ttf"
    tf = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tf.write(data)
    tf.flush()
    tf.close()
    return Path(tf.name).resolve().as_uri()


# Choose fonts for scripts
FONT_MAP = {
    "Hindi": "NotoSansDevanagari-Regular.ttf",
    "Marathi": "NotoSansDevanagari-Regular.ttf",
    "Nepali": "NotoSansDevanagari-Regular.ttf",
    "Sanskrit": "NotoSansDevanagari-Regular.ttf",
    "Maithili": "NotoSansDevanagari-Regular.ttf",
    "Bodo": "NotoSansDevanagari-Regular.ttf",
    "Dogri": "NotoSansDevanagari-Regular.ttf",
    "Konkani": "NotoSansDevanagari-Regular.ttf",
    "Manipuri": "NotoSansDevanagari-Regular.ttf",
    "Bengali": "NotoSansBengali-Regular.ttf",
    "Assamese": "NotoSansBengali-Regular.ttf",
    "Gujarati": "NotoSansGujarati-Regular.ttf",
    "Punjabi": "NotoSansGurmukhi-Regular.ttf",
    "Kannada": "NotoSansKannada-Regular.ttf",
    "Malayalam": "NotoSansMalayalam-Regular.ttf",
    "Tamil": "NotoSansTamil-Regular.ttf",
    "Telugu": "NotoSansTelugu-Regular.ttf",
    "Urdu": "NotoNastaliqUrdu-Regular.ttf",
    "Kashmiri": "NotoNastaliqUrdu-Regular.ttf",
    "Sindhi": "NotoNastaliqUrdu-Regular.ttf",
    "Santali": "NotoSansOlChiki-Regular.ttf",
    "Odia": "NotoSansOriya-Regular.ttf",
    "DEFAULT": "NotoSans-Regular.ttf",
}


def _choose_font_for_lang(tgt_lang: str, fonts_dir: str) -> Optional[str]:
    """Return full path to a font file for the target language."""
    fname = FONT_MAP.get(tgt_lang)
    if fname:
        path = os.path.join(fonts_dir, fname)
        if os.path.isfile(path):
            return path

    for key, fname in FONT_MAP.items():
        if key.lower() in tgt_lang.lower():
            path = os.path.join(fonts_dir, fname)
            if os.path.isfile(path):
                return path

    default = FONT_MAP.get("DEFAULT")
    if default:
        default_path = os.path.join(fonts_dir, default)
        if os.path.isfile(default_path):
            return default_path

    return None


def translate_pdf_bytes_preserve_layout(
    pdf_bytes: bytes, src_lang: str, tgt_lang: str, fonts_dir: str = "./fonts"
) -> io.BytesIO:
    """
    Main helper: translates PDF block-by-block preserving layout.
    Returns io.BytesIO containing the new PDF.
    """
    # Determine font for the target language
    fontfile = _choose_font_for_lang(tgt_lang, fonts_dir)
    fontfile_uri = None

    if fontfile is None:
        print(
            f"[doc_translator] WARNING: No font found for '{tgt_lang}' in {fonts_dir}"
        )
    else:
        print(f"[doc_translator] Using font: {fontfile} for {tgt_lang}")
        fontfile_uri = _fontfile_to_file_uri(
            fontfile
        ) or _copy_font_to_temp_and_get_uri(fontfile)
        if fontfile_uri:
            print(f"[doc_translator] Font URI: {fontfile_uri}")

    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    # Process each page
    for page_idx in range(len(doc)):
        page = doc[page_idx]
        page_rect = page.rect

        # Get all images on the page
        image_rects = _get_image_bboxes_from_page(page)

        # Extract text blocks
        blocks = extract_blocks_with_lines(page)

        # Sort blocks by vertical position (top to bottom) for better ordering
        blocks.sort(key=lambda b: (b["bbox"][1], b["bbox"][0]))

        # Track occupied areas (images + already placed text)
        occupied_rects = image_rects.copy()

        # Store translated blocks with their placement info
        translated_placements = []

        for blk_idx, blk in enumerate(blocks):
            # Build original text from lines
            original_text = " ".join(line["text"] for line in blk["lines"])

            # Translate the text
            translated_text = translate_text(original_text, src_lang, tgt_lang)

            if not translated_text.strip():
                continue

            # Get original font size for consistency
            original_font_size = blk.get("avg_font_size", 12.0)
            if original_font_size == 0 or original_font_size < 6:
                original_font_size = 12.0

            # Use original bbox as starting point
            original_rect = fitz.Rect(blk["bbox"])

            # Find safe placement that doesn't overlap
            safe_rect = _find_safe_placement_rect(
                original_rect, occupied_rects, page_rect, margin=3.0
            )

            # If a safe rect is found, see if we can expand it a bit to allow larger text
            if safe_rect is None:
                print(
                    f"[doc_translator] Warning: Could not find safe placement for block {blk_idx}, using original position"
                )
                safe_rect = original_rect

            # Try to expand available space (so we can fit bigger fonts) while keeping it safe
            expanded_rect = _expand_rect_to_available_space(
                safe_rect,
                occupied_rects,
                page_rect,
                max_expand_pixels=80,
                step=8,
                margin=3.0,
            )

            # Add this rect to occupied areas for next blocks (reserve the expanded rect)
            occupied_rects.append(expanded_rect)

            # Store placement info
            translated_placements.append(
                {
                    "rect": expanded_rect,
                    "text": translated_text,
                    "font_size": original_font_size,
                    "original_rect": original_rect,
                }
            )

        # Now redact all original text in one pass
        for blk in blocks:
            block_rect = fitz.Rect(blk["bbox"])

            # Check if this block overlaps with any images
            has_image_overlap = any(
                _rects_overlap(block_rect, img, margin=0) for img in image_rects
            )

            if not has_image_overlap:
                # Safe to redact entire block
                page.add_redact_annot(block_rect, fill=(1, 1, 1))
            else:
                # Redact line by line, avoiding images
                for line in blk["lines"]:
                    line_rect = fitz.Rect(line["bbox"])
                    line_overlaps_image = any(
                        _rects_overlap(line_rect, img, margin=0) for img in image_rects
                    )

                    if not line_overlaps_image:
                        page.add_redact_annot(line_rect, fill=(1, 1, 1))

        # Apply all redactions at once
        try:
            page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)
        except Exception as e:
            print(f"[doc_translator] Redaction failed: {e}")

        # Insert all translated text with consistent font sizing
        for placement in translated_placements:
            rect = placement["rect"]
            text = placement["text"]
            original_fs = placement["font_size"]

            # Count lines in translated text
            num_lines = max(1, text.count("\n") + 1)

            # Height constraint: give up to ~85% of line-height for font
            height_per_line = rect.height / num_lines
            max_fs_by_height = height_per_line * 0.85

            # Width constraint: estimate average characters per line and compute an approximate font size
            avg_chars_per_line = max(1.0, len(text) / num_lines)
            # Rough estimate: average character width in points is ~0.5 * fontsize (varies by font). We solve for fs such that avg_chars_per_line * (0.5 * fs) <= rect.width
            if avg_chars_per_line > 0:
                max_fs_by_width = (
                    rect.width / avg_chars_per_line
                ) * 1.8  # tuned factor
            else:
                max_fs_by_width = max_fs_by_height

            # Allow slightly larger than original if space permits but cap it
            max_allowed_fs = min(24.0, original_fs * 1.4)

            # Start with the lesser of calculated maxima and the allowed cap
            target_fs = min(max_fs_by_height, max_fs_by_width, max_allowed_fs)

            # Ensure a comfortable minimum for readability
            target_fs = max(8.0, target_fs)

            # If the rect was expanded then we can try starting a little larger to prefer bigger text
            start_fs = min(28.0, target_fs * 1.12)

            # Prepare HTML-safe text
            safe_text = html.escape(text).replace("\n", "<br/>")

            # Try to insert with HTML (it will shrink if needed)
            success_fs = _insert_html_with_shrink(
                page,
                rect,
                safe_text,
                fontfile_uri,
                start_fs=start_fs,
                min_fs=max(6.0, target_fs * 0.55),
            )

            if success_fs == 0:
                # Fallback to insert_textbox - try with the target_fs (rounded)
                print(f"[doc_translator] HTML insertion failed, using textbox fallback")
                try:
                    # insert_textbox uses 'fontsize' in points; convert to int but keep >=8
                    textbox_fs = max(8, int(round(target_fs)))
                    page.insert_textbox(
                        rect,
                        text,
                        fontsize=textbox_fs,
                        align=0,
                        overlay=True,
                    )
                except Exception as e:
                    print(f"[doc_translator] Textbox insertion also failed: {e}")

    # Subset fonts and save
    try:
        doc.subset_fonts()
    except Exception:
        # Not critical
        pass
    out = io.BytesIO()
    doc.save(out)
    doc.close()
    out.seek(0)
    return out
