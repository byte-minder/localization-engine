<!-- Generated using AI -->
<script>
	let displayLanguage = "English";
	let textSize = 14;
	let autoTranslate = false;
	let autoSubtitles = false;
	let autoSync = false;
	let screenReader = false;
	let speechNav = false;
	let highContrast = false;

	const languages = ["English", "Hindi", "Telugu"];
</script>

<header class="app-bar">
	<h1>Settings</h1>
</header>

<main class="container">
	<!-- Language Preferences -->
	<section class="card">
		<h2>Language Preferences</h2>
		<p>Choose your preferred display language.</p>
		<select bind:value={displayLanguage}>
			{#each languages as lang}
				<option value={lang}>{lang}</option>
			{/each}
		</select>
		<button class="add-lang-btn">+ Add Language</button>
	</section>

	<!-- Automation Preferences -->
	<section class="card">
		<h2>Automation</h2>
		<p>Enable automation features to streamline localization workflows.</p>

		<label><input type="checkbox" bind:checked={autoTranslate} /> Auto-translate uploaded content</label>
		<label><input type="checkbox" bind:checked={autoSubtitles} /> Auto-generate subtitles for multimedia</label>
		<label><input type="checkbox" bind:checked={autoSync} /> Sync translations across formats</label>
	</section>

	<!-- Accessibility -->
	<section class="card">
		<h2>Accessibility</h2>
		<p>Adapt your learning experience for better accessibility.</p>

		<label><input type="checkbox" bind:checked={screenReader} /> Enable Screen Reader</label>
		<label><input type="checkbox" bind:checked={speechNav} /> Speech Navigation</label>
		<label><input type="checkbox" bind:checked={highContrast} /> High Contrast Mode</label>

		<div class="slider">
			<label for="text-size-slider">Text Size: {textSize}px</label>
			<input id="text-size-slider" type="range" min="12" max="24" step="1" bind:value={textSize} />
		</div>
	</section>

	<!-- Buttons -->
	<div class="actions">
		<button class="save-btn">Save Changes</button>
		<button class="reset-btn">Reset Defaults</button>
	</div>
</main>

<style>
	.app-bar {
		background: #6200ee;
		color: white;
		padding: 1rem;
		font-size: 1.25rem;
		font-weight: 600;
		box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
	}

	.container {
		padding: 2rem;
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.card {
		background: #fff;
		padding: 1.5rem;
		border-radius: 12px;
		box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	select,
	input[type="checkbox"],
	input[type="range"] {
		margin-top: 0.5rem;
	}

	.add-lang-btn {
		background: #03dac6;
		color: black;
		border: none;
		padding: 0.5rem 1rem;
		border-radius: 8px;
		margin-top: 0.5rem;
		cursor: pointer;
	}

	.actions {
		display: flex;
		justify-content: flex-end;
		gap: 1rem;
		margin-top: 1rem;
	}

	.save-btn {
		background: #6200ee;
		color: white;
		border: none;
		padding: 0.75rem 1.5rem;
		border-radius: 8px;
		cursor: pointer;
	}

	.reset-btn {
		background: #e0e0e0;
		color: black;
		border: none;
		padding: 0.75rem 1.5rem;
		border-radius: 8px;
		cursor: pointer;
	}
</style>
