<script lang="ts">
	export let selectedLanguages: string[] = [];
	const allLanguages = [
		{ code: "hi", name: "Hindi" },
		{ code: "te", name: "Telugu" },
		{ code: "en", name: "English" },
		// Placeholders for other languages
		...Array.from({ length: 19 }, (_, i) => ({
			code: `lang${i + 1}`,
			name: `Future Language ${i + 1}`,
		})),
	];
	function toggleLanguage(code: string) {
		if (selectedLanguages.includes(code)) {
			selectedLanguages = selectedLanguages.filter((lang) => lang !== code);
		} else {
			selectedLanguages = [...selectedLanguages, code];
		}
	}
</script>

<div class="my-6">
	<label for="language-grid" class="block mb-2 font-medium text-gray-700">
		Target Languages
	</label>
	<div
		class="grid grid-cols-[repeat(auto-fill,minmax(150px,1fr))] gap-2"
		id="language-grid"
	>
		{#each allLanguages as lang}
			<button
				class="px-3 py-3 border rounded text-left transition-all cursor-pointer {selectedLanguages.includes(
					lang.code,
				)
					? 'bg-indigo-600 text-white border-indigo-600'
					: 'bg-white text-gray-700 border-gray-300 hover:border-indigo-400'}"
				on:click={() => toggleLanguage(lang.code)}
			>
				{lang.name}
			</button>
		{/each}
	</div>
</div>
