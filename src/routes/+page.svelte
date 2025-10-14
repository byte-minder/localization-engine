<script lang="ts">
	let activeTab: "text" | "pdf" | "audio" = "text";
	let showResults = false;

	function handleAction() {
		showResults = true;
	}

	const languages = ["English", "Hindi", "Telugu"];
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

<main class="container p-6 max-w-3xl mx-auto font-sans">
	<div class="bg-white p-6 rounded-lg shadow-md mb-6">
		<div class="flex items-center gap-4 mb-6">
			<div class="flex-1 flex flex-col">
				<label class="text-xs font-medium text-gray-600 mb-2" for="from-lang"
					>FROM</label
				>
				<select
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
					class="flex items-center justify-center h-[150px] border-2 border-dashed border-gray-300 rounded-lg text-gray-500 cursor-pointer hover:border-indigo-600 hover:text-indigo-600 transition-colors"
				>
					<span>Upload PDF</span>
				</div>
				<div class="flex justify-end gap-2">
					<button
						class="bg-transparent text-indigo-600 font-medium px-4 py-2 rounded hover:bg-indigo-50 transition-colors"
					>
						EXTRACT TEXT
					</button>
					<button
						class="bg-indigo-600 text-white font-medium px-4 py-2 rounded hover:bg-indigo-700 transition-colors"
						on:click={handleAction}
					>
						TRANSLATE
					</button>
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

	{#if showResults}
		<div class="bg-white p-6 rounded-lg shadow-md">
			<div
				class="flex justify-between items-center border-b border-gray-200 pb-2 mb-3"
			>
				<h2 class="text-base font-medium text-gray-600">Translated Output</h2>
				<button
					class="p-1 rounded-full hover:bg-gray-100 transition-colors text-gray-500 hover:text-indigo-600"
					title="Read result aloud"
				>
					🔊
				</button>
			</div>
			<p class="text-sm text-gray-800">
				This is where the translated or transcribed text will appear.
				Placeholder content.
			</p>
		</div>
	{/if}
</main>
