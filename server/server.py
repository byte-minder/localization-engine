import gc
import io
import json
import logging
import shutil
from typing import Dict, List, Optional

import torch
import torchaudio
from flask import Flask, jsonify, request
from flask_cors import CORS
from IndicTransToolkit.processor import IndicProcessor
from transformers import (AutoModelForSeq2SeqLM, AutoTokenizer,
                          WhisperForConditionalGeneration, WhisperProcessor)

transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.DEBUG)


# ----------------------
# Flask & CORS setup
# ----------------------
app = Flask(__name__)
CORS(app)  # Allow all origins for frontend

# ----------------------
# Device
# ----------------------
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[INIT] USING DEVICE: {DEVICE}")
if DEVICE == "cuda":
    print(f"[INIT] GPU: {torch.cuda.get_device_name(0)}")
    print(f"[INIT] CUDA Version: {torch.version.cuda}")

# Check ffmpeg
FFMPEG_PATH = shutil.which("ffmpeg")
if FFMPEG_PATH is None:
    raise RuntimeError("ffmpeg not found in PATH. Please install ffmpeg.")
print(f"[INIT] Using ffmpeg at: {FFMPEG_PATH}")

# Model paths
WHISPER_MODEL = "./models/whisper-medium"
MODEL_PATH_EN_INDIC = "./models/indictrans2-en-indic-1B"
MODEL_PATH_INDIC_EN = "./models/indictrans2-indic-en-1B"

# ----------------------
# Language codes
# ----------------------
LANG_CODES = {
    "Assamese": "asm_Beng",
    "Bengali": "ben_Beng",
    "English": "eng_Latn",
    "Gujarati": "guj_Gujr",
    "Hindi": "hin_Deva",
    "Kannada": "kan_Knda",
    "Malayalam": "mal_Mlym",
    "Marathi": "mar_Deva",
    "Nepali": "npi_Deva",
    "Odia": "ory_Orya",
    "Punjabi": "pan_Guru",
    "Sanskrit": "san_Deva",
    "Tamil": "tam_Taml",
    "Telugu": "tel_Telu",
    "Urdu": "urd_Arab",
    "Kashmiri": "kas_Arab",
    "Maithili": "mai_Deva",
    "Sindhi": "snd_Arab",
    "Bodo": "brx_Deva",
    "Dogri": "doi_Deva",
    "Konkani": "kok_Deva",
    "Manipuri (Bengali)": "mni_Beng",
    "Manipuri (Meetei)": "mni_Mtei",
    "Santali": "sat_Olck",
}


# ----------------------
# Model cache
# ----------------------
class ModelCache:
    def __init__(self):
        self.whisper_processor: Optional[WhisperProcessor] = None
        self.whisper_model: Optional[WhisperForConditionalGeneration] = None

        self.tok_en_indic: Optional[AutoTokenizer] = None
        self.model_en_indic: Optional[AutoModelForSeq2SeqLM] = None
        self.tok_indic_en: Optional[AutoTokenizer] = None
        self.model_indic_en: Optional[AutoModelForSeq2SeqLM] = None
        self.indic_processor: Optional[IndicProcessor] = None

    # ------------- Whisper -------------
    def load_whisper(self):
        if self.whisper_processor is None or self.whisper_model is None:
            print("[LAZY] Loading Whisper-Medium model...")
            self.whisper_processor = WhisperProcessor.from_pretrained(
                WHISPER_MODEL, local_files_only=True
            )
            self.whisper_model = WhisperForConditionalGeneration.from_pretrained(
                WHISPER_MODEL,
                local_files_only=True,
                dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
            )
            self.whisper_model = self.whisper_model.to(DEVICE)
            print(f"[LAZY] Whisper model loaded on {DEVICE}")
        return self.whisper_processor, self.whisper_model

    def unload_whisper(self):
        if self.whisper_model is not None:
            print("[CLEANUP] Unloading Whisper model...")
            del self.whisper_model
            del self.whisper_processor
            self.whisper_model = None
            self.whisper_processor = None
        gc.collect()
        if DEVICE == "cuda":
            torch.cuda.empty_cache()
        print("[CLEANUP] Whisper model unloaded.")

    # ------------- Translation -------------
    def load_translation_models(self, direction):

        if self.indic_processor is None:
            print("[LAZY] Loading IndicProcessor...")
            self.indic_processor = IndicProcessor(inference=True)

        if direction == "en_to_indic":
            if self.tok_en_indic is None or self.model_en_indic is None:
                print("[LAZY] Loading EN→Indic translation model...")
                self.tok_en_indic = AutoTokenizer.from_pretrained(
                    MODEL_PATH_EN_INDIC, local_files_only=True, trust_remote_code=True
                )
                self.model_en_indic = AutoModelForSeq2SeqLM.from_pretrained(
                    MODEL_PATH_EN_INDIC,
                    local_files_only=True,
                    trust_remote_code=True,
                    dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
                )
                self.model_en_indic = self.model_en_indic.to(DEVICE)
                assert self.model_en_indic is not None, "Model did not load correctly!"
                print(f"[LAZY] EN→Indic model loaded on {DEVICE}")
            return self.tok_en_indic, self.model_en_indic, self.indic_processor

        elif direction == "indic_to_en":
            if self.tok_indic_en is None or self.model_indic_en is None:
                print("[LAZY] Loading Indic→EN translation model...")
                self.tok_indic_en = AutoTokenizer.from_pretrained(
                    MODEL_PATH_INDIC_EN, local_files_only=True, trust_remote_code=True
                )
                self.model_indic_en = AutoModelForSeq2SeqLM.from_pretrained(
                    MODEL_PATH_INDIC_EN,
                    local_files_only=True,
                    trust_remote_code=True,
                    dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
                )
                self.model_indic_en = self.model_indic_en.to(DEVICE)
                assert self.model_indic_en is not None, "Model did not load correctly!"
                print(f"[LAZY] Indic→EN model loaded on {DEVICE}")
            return self.tok_indic_en, self.model_indic_en, self.indic_processor

    def unload_translation(self):
        if self.model_en_indic:
            del self.model_en_indic, self.tok_en_indic
            self.model_en_indic = None
            self.tok_en_indic = None
        if self.model_indic_en:
            del self.model_indic_en, self.tok_indic_en
            self.model_indic_en = None
            self.tok_indic_en = None
        if self.indic_processor:
            del self.indic_processor
            self.indic_processor = None
        gc.collect()
        if DEVICE == "cuda":
            torch.cuda.empty_cache()
        print("[CLEANUP] Translation models unloaded.")


cache = ModelCache()


# ----------------------
# Helpers
# ----------------------
def normalize_lang(lang):
    return LANG_CODES.get(lang, lang)


def translate_text(text, src_lang, tgt_lang):
    src_code = LANG_CODES[src_lang]
    tgt_code = LANG_CODES[tgt_lang]

    print(f"[TRANSLATE] Request: '{text}' from {src_lang} → {tgt_lang}")

    try:
        # Load processor & model
        ip = cache.indic_processor or IndicProcessor(inference=True)
        if src_code.startswith("eng") and not tgt_code.startswith("eng"):
            tok, model, _ = cache.load_translation_models("en_to_indic")
        elif not src_code.startswith("eng") and tgt_code.startswith("eng"):
            tok, model, _ = cache.load_translation_models("indic_to_en")
        else:
            # Indic→Indic: relay via English
            mid = translate_text(text, src_lang, "English")
            return translate_text(mid, "English", tgt_lang)

        # Put model in eval and disable caching to avoid past_key_values issues
        model.eval()
        # Ensure both config and runtime generation request use_cache=False
        try:
            model.config.use_cache = False
        except Exception:
            # some model wrappers might not have config; ignore if not present
            pass

        # Preprocess
        if ip:
            batch = ip.preprocess_batch([text], src_lang=src_code, tgt_lang=tgt_code)
        else:
            batch = [text]

        # Build inputs
        if isinstance(batch, dict):
            inputs = {}
            for k, v in batch.items():
                if isinstance(v, torch.Tensor):
                    inputs[k] = v.to(DEVICE)
                else:
                    try:
                        inputs[k] = torch.tensor(v, device=DEVICE)
                    except Exception:
                        continue
        else:
            enc = tok(
                batch,
                truncation=True,
                padding="longest",
                return_tensors="pt",
                return_attention_mask=True,
                max_length=256,
            )
            inputs = {
                k: v.to(DEVICE) for k, v in enc.items() if isinstance(v, torch.Tensor)
            }

        # Sanity: must have input_ids
        if "input_ids" not in inputs or inputs["input_ids"] is None:
            raise RuntimeError(
                "tokenizer/processor did not return 'input_ids'. Check input types and processor output."
            )

        # Ensure tensors are on the same device as the model
        model_device = next(model.parameters()).device
        for k, v in list(inputs.items()):
            if isinstance(v, torch.Tensor):
                inputs[k] = v.to(model_device)

        gen_kwargs = {
            "input_ids": inputs.get("input_ids"),
            # explicitly disable use_cache to avoid past_key_values access in forward
            "use_cache": False,
            # safe defaults:
            "num_beams": 5,
            "max_length": 256,
            "num_return_sequences": 1,
        }
        if inputs.get("attention_mask") is not None:
            gen_kwargs["attention_mask"] = inputs.get("attention_mask")

        with torch.no_grad():
            outputs = model.generate(**gen_kwargs)

        print("[DEBUG] outputs:", outputs)
        if outputs is not None:
            print("[DEBUG] outputs shape:", getattr(outputs, "shape", "n/a"))
        else:
            print("[DEBUG] outputs is None!")

        decoded = tok.batch_decode(outputs, skip_special_tokens=True)
        if ip:
            decoded = ip.postprocess_batch(decoded, lang=tgt_code)
        print(decoded[0])
        return decoded[0]

    except Exception as e:
        print("[ERROR] IndicTrans2 translation failed:", e)
        import traceback

        traceback.print_exc()
        return "[Translation Error]"


# ----------------------
# Flask endpoints
# ----------------------
@app.route("/translate", methods=["POST"])
def translate_endpoint():
    data = request.get_json()
    print(f"[TRANSLATE ENDPOINT] Raw data: {request.data}")
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    text = data["text"]
    src_lang = data.get("src_lang", "English")
    tgt_lang = data.get("tgt_lang", "English")

    print(
        f"[TRANSLATE ENDPOINT] Received text: '{text[:50]}...' | {src_lang} → {tgt_lang}"
    )
    translated = translate_text(text, src_lang, tgt_lang)
    cache.unload_translation()

    return jsonify(
        {
            "detected_lang": src_lang,
            "translation": translated,
            "translated_to": tgt_lang,
        }
    )


# Keep Whisper endpoints unchanged...
# transcribe_with_whisper(), load_audio(), /transcribe, /unload

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
