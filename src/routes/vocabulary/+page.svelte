<!-- Tailwind converted -->
<script>
	let activeTab = "wordlist";
	let selectedSector = "Healthcare";
	let selectedLanguage = "English";
	let searchQuery = "";

	const sectors = [
		"Healthcare",
		"Construction",
		"IT",
		"Agriculture",
		"Hospitality",
	];
	const languages = ["English", "Hindi", "Telugu"];

	function addLanguage() {
		const lang = prompt("Add a language (e.g. Spanish)");
		if (lang) {
			const trimmed = lang.trim();
			if (trimmed && !languages.includes(trimmed)) languages.push(trimmed);
		}
	}

	function setTab(tab) {
		activeTab = tab;
	}
</script>

<svelte:head>
	<title>Vocabulary Bank</title>
</svelte:head>

<header class="bg-indigo-600 text-white shadow-sm">
	<div class="max-w-6xl mx-auto px-4 py-4">
		<h1 class="text-lg font-semibold">Vocabulary Bank</h1>
	</div>
</header>

<main class="max-w-6xl mx-auto px-4 py-6 space-y-6">
	<!-- Filters -->
	<section class="flex flex-col md:flex-row md:items-center gap-4 md:gap-6">
		<div class="flex items-center gap-3">
			<label for="sector-select" class="text-sm font-medium text-gray-700"
				>Sector</label
			>
			<select
				id="sector-select"
				bind:value={selectedSector}
				class="rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
			>
				{#each sectors as sector}
					<option value={sector}>{sector}</option>
				{/each}
			</select>
		</div>

		<div class="flex items-center gap-3">
			<label for="language-select" class="text-sm font-medium text-gray-700"
				>Language</label
			>
			<select
				id="language-select"
				bind:value={selectedLanguage}
				class="rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
			>
				{#each languages as lang}
					<option value={lang}>{lang}</option>
				{/each}
			</select>

			<button
				on:click={addLanguage}
				class="ml-2 inline-flex items-center gap-2 rounded-md bg-emerald-400 px-3 py-2 text-sm font-medium text-black hover:bg-emerald-300 focus:outline-none focus:ring-2 focus:ring-emerald-300"
			>
				+ Add
			</button>
		</div>

		<div class="flex-1">
			<input
				type="text"
				placeholder="Search for a word..."
				bind:value={searchQuery}
				class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
				aria-label="Search vocabulary"
			/>
		</div>
	</section>

	<!-- Tabs -->
	<nav class="flex gap-4 border-b border-gray-200">
		<button
			role="tab"
			aria-selected={activeTab === "wordlist"}
			class="-mb-px px-3 py-2 text-sm font-medium focus:outline-none"
			class:!text-indigo-600={activeTab === "wordlist"}
			class:!border-b-2={activeTab === "wordlist"}
			class:!border-indigo-600={activeTab === "wordlist"}
			on:click={() => setTab("wordlist")}
		>
			Word List
		</button>

		<button
			role="tab"
			aria-selected={activeTab === "examples"}
			class="-mb-px px-3 py-2 text-sm font-medium focus:outline-none"
			class:!text-indigo-600={activeTab === "examples"}
			class:!border-b-2={activeTab === "examples"}
			class:!border-indigo-600={activeTab === "examples"}
			on:click={() => setTab("examples")}
		>
			Usage Examples
		</button>

		<button
			role="tab"
			aria-selected={activeTab === "audio"}
			class="-mb-px px-3 py-2 text-sm font-medium focus:outline-none"
			class:!text-indigo-600={activeTab === "audio"}
			class:!border-b-2={activeTab === "audio"}
			class:!border-indigo-600={activeTab === "audio"}
			on:click={() => setTab("audio")}
		>
			Audio Practice
		</button>
	</nav>

	<section>
		{#if activeTab === "wordlist"}
			<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
				<div class="bg-white rounded-lg shadow p-4">
					<h3 class="text-sm font-semibold text-gray-800">Welding</h3>
					<p class="mt-1 text-xs text-gray-600">
						Translation: वेल्डिंग (Hindi)
					</p>
					<button
						class="mt-3 inline-flex items-center gap-2 rounded-md bg-indigo-600 px-3 py-1 text-xs font-medium text-white hover:bg-indigo-700"
						>🔊 Play</button
					>
				</div>

				<div class="bg-white rounded-lg shadow p-4">
					<h3 class="text-sm font-semibold text-gray-800">Safety Gear</h3>
					<p class="mt-1 text-xs text-gray-600">
						Translation: सुरक्षा उपकरण (Hindi)
					</p>
					<button
						class="mt-3 inline-flex items-center gap-2 rounded-md bg-indigo-600 px-3 py-1 text-xs font-medium text-white hover:bg-indigo-700"
						>🔊 Play</button
					>
				</div>
			</div>
		{:else if activeTab === "examples"}
			<div class="space-y-4">
				<div class="bg-white rounded-lg shadow p-4">
					<p class="text-sm font-medium text-gray-800">Word: Safety Gear</p>
					<p class="mt-2 text-sm text-gray-700">
						“Always wear safety gear before operating heavy machinery.”
					</p>
					<p class="mt-1 text-sm text-gray-600 italic">
						“भारी मशीन चलाने से पहले हमेशा सुरक्षा उपकरण पहनें।”
					</p>
				</div>
			</div>
		{:else}
			<div class="space-y-4">
				<div
					class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center text-sm text-gray-600"
				>
					Upload Audio (MP3, WAV, OGG)
				</div>
				<div class="flex gap-3">
					<button
						class="rounded-md bg-gray-100 px-3 py-2 text-sm font-medium hover:bg-gray-200"
						>Upload</button
					>
					<button
						class="rounded-md bg-indigo-600 px-3 py-2 text-sm font-medium text-white hover:bg-indigo-700"
						>Play</button
					>
					<button
						class="rounded-md bg-emerald-400 px-3 py-2 text-sm font-medium text-black hover:bg-emerald-300"
						>Record New</button
					>
				</div>
			</div>
		{/if}
	</section>
</main>
