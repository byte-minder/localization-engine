<script lang="ts">
	export let selectedLanguages: string[] = [];

	const allLanguages = [
		
		{ code: 'hi', name: 'Hindi' },
		{ code: 'te', name: 'Telugu' },
		{ code: 'en', name: 'English' },
		// Placeholders for other languages
		...Array.from({ length: 19 }, (_, i) => ({ code: `lang${i + 1}`, name: `Future Language ${i + 1}` }))
	];

	function toggleLanguage(code: string) {
		if (selectedLanguages.includes(code)) {
			selectedLanguages = selectedLanguages.filter((lang) => lang !== code);
		} else {
			selectedLanguages = [...selectedLanguages, code];
		}
	}
</script>

<div class="lang-selector">
	<label for="language-grid">Target Languages</label>
	<div class="grid" id="language-grid">
		{#each allLanguages as lang}
			<button
				class:selected={selectedLanguages.includes(lang.code)}
				on:click={() => toggleLanguage(lang.code)}
			>
				{lang.name}
			</button>
		{/each}
	</div>
</div>

<style>
	.lang-selector {
		margin: 1.5rem 0;
	}
	label {
		display: block;
		margin-bottom: 0.5rem;
		font-weight: 500;
	}
	.grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
		gap: 0.5rem;
	}
	button {
		padding: 0.75rem;
		border: 1px solid #ced4da;
		border-radius: 4px;
		background-color: #fff;
		cursor: pointer;
		text-align: left;
		transition: all 0.2s;
	}
	button:hover {
		border-color: #80bdff;
	}
	button.selected {
		background-color: #007bff;
		color: white;
		border-color: #007bff;
	}
</style>