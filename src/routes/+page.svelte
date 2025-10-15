<script lang="ts">
	import { onDestroy } from "svelte";

	let activeTab: "text" | "pdf" | "audio" = "text";
	let showResults = false;
	let fromLang = "English";
	let toLang = "Hindi";
	let inputText = "";
	let translatedText = "";

	const languages = [
		"Assamese",
		"Bengali",
		"English",
		"Gujarati",
		"Hindi",
		"Kannada",
		"Malayalam",
		"Marathi",
		"Nepali",
		"Odia",
		"Punjabi",
		"Sanskrit",
		"Tamil",
		"Telugu",
		"Urdu",
		"Kashmiri",
		"Maithili",
		"Sindhi",
		"Bodo",
		"Dogri",
		"Konkani",
		"Manipuri",
		"Santali",
	];

	// PDF related
	let selectedPdf: File | null = null;
	let pdfPreviewUrl: string | null = null; // local preview of uploaded PDF (optional)
	let translatedPdfUrl: string | null = null; // object URL for translated PDF
	let translating = false;
	let errorMsg: string | null = null;
	let downloadFileName = "translated.pdf";

	// Clean up object URLs on destroy
	onDestroy(() => {
		if (pdfPreviewUrl) URL.revokeObjectURL(pdfPreviewUrl);
		if (translatedPdfUrl) URL.revokeObjectURL(translatedPdfUrl);
	});

	// TEXT translation (existing)
	async function handleAction() {
		errorMsg = null;
		if (activeTab === "text" && inputText.trim()) {
			try {
				// Call the /translate endpoint
				const res = await fetch("http://localhost:5000/translate", {
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({
						text: inputText,
						src_lang: fromLang,
						tgt_lang: toLang,
					}),
				});

				const data = await res.json();
				if (res.ok) {
					translatedText = data.translation;
					showResults = true;
				} else {
					console.error("Translation failed:", data.error);
					errorMsg = data.error || "Translation failed";
				}
			} catch (err) {
				console.error("Error calling server:", err);
				errorMsg = "Server error while translating text.";
			}
		} else if (activeTab === "pdf") {
			// fallback if user clicks old translate button: start PDF flow
			await uploadAndTranslatePdf();
		} else {
			// For AUDIO (placeholder)
			showResults = true;
			translatedText = "Translation placeholder (audio tab)";
		}
	}

	// File input change
	function onPdfSelected(e: Event) {
		errorMsg = null;
		const input = e.target as HTMLInputElement;
		const file = input.files && input.files[0];
		if (!file) return;
		if (file.type !== "application/pdf") {
			errorMsg = "Please upload a PDF file.";
			selectedPdf = null;
			return;
		}
		selectedPdf = file;

		// preview the original PDF in an iframe (optional)
		if (pdfPreviewUrl) {
			URL.revokeObjectURL(pdfPreviewUrl);
			pdfPreviewUrl = null;
		}
		pdfPreviewUrl = URL.createObjectURL(file);
	}

	// Drag & drop handlers (optional)
	function handleDrop(event: DragEvent) {
		event.preventDefault();
		event.stopPropagation();
		errorMsg = null;
		const dt = event.dataTransfer;
		if (!dt) return;
		const file = dt.files && dt.files[0];
		if (!file) return;
		if (file.type !== "application/pdf") {
			errorMsg = "Please drop a PDF file.";
			selectedPdf = null;
			return;
		}
		selectedPdf = file;
		if (pdfPreviewUrl) {
			URL.revokeObjectURL(pdfPreviewUrl);
		}
		pdfPreviewUrl = URL.createObjectURL(file);
	}

	function handleDragOver(event: DragEvent) {
		event.preventDefault();
		event.dataTransfer!.dropEffect = "copy";
	}

	// Upload PDF and receive translated PDF blob
	async function uploadAndTranslatePdf() {
		errorMsg = null;
		showResults = false;
		translatedText = "";
		if (!selectedPdf) {
			errorMsg = "No PDF selected. Please upload a PDF first.";
			return;
		}
		translating = true;

		try {
			const form = new FormData();
			form.append("file", selectedPdf);
			form.append("src_lang", fromLang);
			form.append("tgt_lang", toLang);

			// Adjust URL to your server endpoint; this example uses the advanced endpoint
			const res = await fetch(
				"http://localhost:5000/translate-document-advanced",
				{
					method: "POST",
					body: form,
				},
			);

			if (!res.ok) {
				// try to parse JSON error
				let errText = `Server returned ${res.status}`;
				try {
					const errJson = await res.json();
					errText = errJson.error || JSON.stringify(errJson);
				} catch (e) {
					// not JSON
					errText = await res.text();
				}
				throw new Error(errText);
			}

			const blob = await res.blob();
			// optional: infer filename from content-disposition
			const cd = res.headers.get("content-disposition");
			if (cd) {
				const m = cd.match(/filename\*?=(?:UTF-8'')?["']?([^;"']+)/i);
				if (m && m[1]) {
					downloadFileName = decodeURIComponent(m[1]);
				}
			}

			// revoke old translated URL
			if (translatedPdfUrl) {
				URL.revokeObjectURL(translatedPdfUrl);
			}
			translatedPdfUrl = URL.createObjectURL(blob);

			// show embedded viewer and enable download
			showResults = true;
			translatedText = `Translated PDF ready — use the Preview / Download buttons.`;

			// auto-download? Uncomment if you want immediate download:
			// const a = document.createElement('a'); a.href = translatedPdfUrl; a.download = downloadFileName; a.click();
		} catch (err) {
			console.error("PDF translation error:", err);
			errorMsg = (err as Error).message || "PDF translation failed";
		} finally {
			translating = false;
		}
	}

	function downloadTranslatedPdf() {
		if (!translatedPdfUrl) return;
		const a = document.createElement("a");
		a.href = translatedPdfUrl;
		a.download =
			downloadFileName || `translated_${selectedPdf?.name ?? "document"}`;
		document.body.appendChild(a);
		a.click();
		a.remove();
	}

	function clearPdfSelection() {
		selectedPdf = null;
		if (pdfPreviewUrl) {
			URL.revokeObjectURL(pdfPreviewUrl);
			pdfPreviewUrl = null;
		}
		if (translatedPdfUrl) {
			URL.revokeObjectURL(translatedPdfUrl);
			translatedPdfUrl = null;
		}
		showResults = false;
		errorMsg = null;
		translatedText = "";
	}
</script>

<svelte:head>
	<title>Localization Engine</title>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="" />
	<link
		href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap"
		rel="stylesheet"
	/>
</svelte:head>

<header class="bg-indigo-600 px-6 py-4 shadow-lg">
	<h1 class="text-white text-xl font-medium">Localization Engine</h1>
</header>

<main class="container p-6 max-w-4xl mx-auto font-sans">
	<div class="bg-white p-6 rounded-lg shadow-md mb-6">
		<div class="flex items-center gap-4 mb-6">
			<div class="flex-1 flex flex-col">
				<label class="text-xs font-medium text-gray-600 mb-2" for="from-lang"
					>FROM</label
				>
				<select
					bind:value={fromLang}
					class="p-2 text-sm bg-white border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
					id="from-lang"
				>
					{#each languages as lang}
						<option>{lang}</option>
					{/each}
				</select>
			</div>

			<div class="text-2xl text-gray-400 mt-6">→</div>

			<div class="flex-1 flex flex-col">
				<label class="text-xs font-medium text-gray-600 mb-2" for="to-lang"
					>TO</label
				>
				<select
					bind:value={toLang}
					class="p-2 text-sm bg-white border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
					id="to-lang"
				>
					{#each languages as lang}
						<option>{lang}</option>
					{/each}
				</select>
			</div>
		</div>

		<div class="flex border-b-2 border-gray-200 mb-4">
			<button
				class="flex-1 py-3 font-medium text-sm transition-colors {activeTab ===
				'text'
					? 'text-indigo-600 border-b-2 border-indigo-600 -mb-0.5'
					: 'text-gray-500 hover:text-gray-700'}"
				on:click={() => (activeTab = "text")}
			>
				TEXT
			</button>
			<button
				class="flex-1 py-3 font-medium text-sm transition-colors {activeTab ===
				'pdf'
					? 'text-indigo-600 border-b-2 border-indigo-600 -mb-0.5'
					: 'text-gray-500 hover:text-gray-700'}"
				on:click={() => (activeTab = "pdf")}
			>
				PDF
			</button>
			<button
				class="flex-1 py-3 font-medium text-sm transition-colors {activeTab ===
				'audio'
					? 'text-indigo-600 border-b-2 border-indigo-600 -mb-0.5'
					: 'text-gray-500 hover:text-gray-700'}"
				on:click={() => (activeTab = "audio")}
			>
				AUDIO
			</button>
		</div>

		<div class="flex flex-col gap-4">
			{#if activeTab === "text"}
				<textarea
					bind:value={inputText}
					class="w-full min-h-[150px] p-4 border border-gray-300 rounded resize-y focus:outline-none focus:ring-2 focus:ring-indigo-500"
					placeholder="Enter text to translate..."
				></textarea>
				<div class="flex justify-end gap-2">
					<button
						class="bg-transparent text-indigo-600 font-medium px-4 py-2 rounded hover:bg-indigo-50 transition-colors"
					>
						PLAY (TTS)
					</button>
					<button
						class="bg-indigo-600 text-white font-medium px-4 py-2 rounded hover:bg-indigo-700 transition-colors"
						on:click={handleAction}
					>
						TRANSLATE
					</button>
				</div>
			{/if}

			{#if activeTab === "pdf"}
				<div
					on:drop|preventDefault={handleDrop}
					on:dragover|preventDefault={handleDragOver}
					class="flex flex-col gap-3"
				>
					<label
						class="flex items-center justify-center h-[180px] border-2 border-dashed border-gray-300 rounded-lg text-gray-500 cursor-pointer hover:border-indigo-600 hover:text-indigo-600 transition-colors"
					>
						<input
							type="file"
							accept="application/pdf"
							on:change={onPdfSelected}
							class="hidden"
						/>
						<div class="text-center">
							<div class="text-lg font-medium">Upload PDF</div>
							<div class="text-xs mt-1">Drop a PDF here or click to select</div>
							{#if selectedPdf}
								<div class="mt-2 text-sm text-gray-700">{selectedPdf.name}</div>
							{/if}
						</div>
					</label>

					<div class="flex justify-end gap-2">
						<button
							class="bg-transparent text-indigo-600 font-medium px-4 py-2 rounded hover:bg-indigo-50 transition-colors"
							on:click={() => {
								if (!selectedPdf) errorMsg = "Please choose a PDF first.";
								else {
									// Optionally extract text first by calling a backend endpoint
									// For now just show preview
									showResults = !!pdfPreviewUrl;
								}
							}}
						>
							PREVIEW
						</button>

						<button
							class="bg-indigo-600 text-white font-medium px-4 py-2 rounded hover:bg-indigo-700 transition-colors"
							on:click={uploadAndTranslatePdf}
							disabled={translating}
						>
							{#if translating}TRANSLATING...{:else}TRANSLATE{/if}
						</button>

						<button
							class="bg-gray-100 text-gray-700 font-medium px-4 py-2 rounded hover:bg-gray-200 transition-colors"
							on:click={clearPdfSelection}
						>
							CLEAR
						</button>
					</div>
				</div>
			{/if}

			{#if activeTab === "audio"}
				<div
					class="flex items-center justify-center h-[150px] border-2 border-dashed border-gray-300 rounded-lg text-gray-500 cursor-pointer hover:border-indigo-600 hover:text-indigo-600 transition-colors"
				>
					<span>Upload Audio (MP3/WAV/OGG)</span>
				</div>
				<div class="flex justify-end gap-2">
					<button
						class="bg-transparent text-indigo-600 font-medium px-4 py-2 rounded hover:bg-indigo-50 transition-colors"
					>
						PLAY (TTS)
					</button>
					<button
						class="bg-indigo-600 text-white font-medium px-4 py-2 rounded hover:bg-indigo-700 transition-colors"
						on:click={handleAction}
					>
						TRANSCRIBE
					</button>
				</div>
			{/if}
		</div>
	</div>

	{#if errorMsg}
		<div class="bg-red-50 border border-red-200 text-red-700 p-4 rounded mb-4">
			<strong>Error:</strong>
			{errorMsg}
		</div>
	{/if}

	{#if showResults}
		<div class="bg-white p-6 rounded-lg shadow-md">
			<div
				class="flex justify-between items-center border-b border-gray-200 pb-2 mb-3"
			>
				<h2 class="text-base font-medium text-gray-600">Translated Output</h2>
				<div class="flex items-center gap-2">
					{#if translatedPdfUrl}
						<button
							class="bg-white border px-3 py-1 rounded hover:bg-gray-50"
							on:click={() => {
								/* open in new tab */
								if (translatedPdfUrl) window.open(translatedPdfUrl, "_blank");
							}}
						>
							Open in new tab
						</button>

						<button
							class="bg-indigo-600 text-white px-3 py-1 rounded hover:bg-indigo-700"
							on:click={downloadTranslatedPdf}
						>
							Download PDF
						</button>
					{/if}
					<button
						class="p-1 rounded-full hover:bg-gray-100 transition-colors text-gray-500 hover:text-indigo-600"
						title="Read result aloud"
					>
						🔊
					</button>
				</div>
			</div>

			{#if translatedPdfUrl}
				<div class="mb-4">
					<!-- Embedded viewer -->
					<iframe
						src={translatedPdfUrl}
						class="w-full h-[600px] border"
						title="Translated PDF Preview"
					></iframe>
				</div>
				<p class="text-sm text-gray-600 mb-0">
					Preview of the translated PDF above.
				</p>
			{:else}
				<p class="text-sm text-gray-800">{translatedText}</p>
			{/if}
		</div>
	{/if}
</main>

<style>
	/* keep a small amount of custom style */
	iframe {
		border: 1px solid #e5e7eb;
	}
</style>
