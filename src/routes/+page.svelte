<script lang="ts">
	let activeTab: 'text' | 'pdf' | 'audio' = 'text';
	let showResults = false;

	function handleAction() {
		showResults = true;
	}

	const languages = ['English', 'Hindi', 'Telugu'];
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

<header class="app-bar">
	<h1>Localization Engine</h1>
</header>

<main class="container">
	
	<div class="card">
	
		<div class="language-selectors">
			<div class="select-wrapper">
				<label for="from-lang">FROM</label>
				<select id="from-lang">
					{#each languages as lang}
						<option>{lang}</option>
					{/each}
				</select>
			</div>

			<div class="icon-swap">→</div>

			<div class="select-wrapper">
				<label for="to-lang">TO</label>
				<select id="to-lang">
					{#each languages as lang}
						<option>{lang}</option>
					{/each}
				</select>
			</div>
		</div>

		<div class="tabs">
			<button class:active={activeTab === 'text'} on:click={() => (activeTab = 'text')}>TEXT</button>
			<button class:active={activeTab === 'pdf'} on:click={() => (activeTab = 'pdf')}>PDF</button>
			<button class:active={activeTab === 'audio'} on:click={() => (activeTab = 'audio')}>AUDIO</button>
		</div>

		<div class="interaction-area">
			{#if activeTab === 'text'}
				<textarea placeholder="Enter text to translate..."></textarea>
				<div class="actions">
					<button class="btn-text">PLAY (TTS)</button>
					<button class="btn-contained" on:click={handleAction}>TRANSLATE</button>
				</div>
			{/if}

			{#if activeTab === 'pdf'}
				<div class="upload-placeholder">
					<span>Upload PDF</span>
				</div>
				<div class="actions">
					<button class="btn-text">EXTRACT TEXT</button>
					<button class="btn-contained" on:click={handleAction}>TRANSLATE</button>
				</div>
			{/if}

			{#if activeTab === 'audio'}
				<div class="upload-placeholder">
					<span>Upload Audio (MP3/WAV/OGG)</span>
				</div>
				<div class="actions">
					<button class="btn-text">PLAY (TTS)</button>
					<button class="btn-contained" on:click={handleAction}>TRANSCRIBE</button>
				</div>
			{/if}
		</div>
	</div>

	{#if showResults}
		<div class="card results-card">
			<div class="results-header">
				<h2>Translated Output</h2>
				<button class="icon-button" title="Read result aloud">🔊</button>
			</div>
			<p class="results-text">
				This is where the translated or transcribed text will appear. Placeholder content.
			</p>
		</div>
	{/if}
</main>

<style>
	.container {
		padding: 2rem;
		max-width: 800px;
		margin: 0 auto;
		font-family: 'Roboto', sans-serif;
	}

	.app-bar {
		background: var(--md-primary);
		color: var(--md-on-primary);
		padding: 1rem 2rem;
		font-size: 1.25rem;
		font-weight: 500;
		box-shadow: var(--md-shadow-md);
	}

	.card {
		background: var(--md-surface);
		padding: 1.5rem;
		border-radius: var(--md-radius-md);
		box-shadow: var(--md-shadow-sm);
		margin-bottom: 1.5rem;
	}

	
	.language-selectors {
		display: flex;
		align-items: center;
		gap: 1rem;
		margin-bottom: 1.5rem;
	}
	.select-wrapper {
		flex: 1;
		display: flex;
		flex-direction: column;
	}
	.select-wrapper label {
		font-size: 0.75rem;
		color: var(--text-secondary);
		margin-bottom: 0.25rem;
	}
	.select-wrapper select {
		padding: 0.5rem;
		border-radius: var(--md-radius-sm);
		border: 1px solid #ccc;
		background: var(--md-surface);
		color: var(--md-on-surface);
	}

	.icon-swap {
		font-size: 1.5rem;
		color: var(--text-secondary);
	}

	.tabs {
		display: flex;
		border-bottom: 2px solid #eee;
		margin-bottom: 1rem;
	}
	.tabs button {
		flex: 1;
		background: none;
		border: none;
		padding: 0.75rem 0;
		font-weight: 500;
		color: var(--text-secondary);
		cursor: pointer;
		transition: color 0.2s;
	}
	.tabs button.active {
		color: var(--md-primary);
		border-bottom: 2px solid var(--md-primary);
	}

	.interaction-area {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	textarea {
		width: 100%;
		min-height: 150px;
		padding: 1rem;
		border-radius: var(--md-radius-sm);
		border: 1px solid #ccc;
		resize: vertical;
		background: var(--md-surface);
		color: var(--md-on-surface);
	}


	.upload-placeholder {
		display: flex;
		align-items: center;
		justify-content: center;
		height: 150px;
		border: 2px dashed #ccc;
		border-radius: var(--md-radius-md);
		color: var(--text-secondary);
		cursor: pointer;
		transition: border-color 0.2s, color 0.2s;
	}
	.upload-placeholder:hover {
		border-color: var(--md-primary);
		color: var(--md-primary);
	}

	
	.actions {
		display: flex;
		justify-content: flex-end;
		gap: 0.5rem;
	}
	.btn-text {
		background: transparent;
		color: var(--md-primary);
		font-weight: 500;
		padding: 0.5rem 1rem;
		border-radius: var(--md-radius-sm);
		cursor: pointer;
	}
	.btn-contained {
		background: var(--md-primary);
		color: var(--md-on-primary);
		padding: 0.5rem 1rem;
		border-radius: var(--md-radius-sm);
		font-weight: 500;
		cursor: pointer;
	}
	.btn-contained:hover {
		opacity: 0.9;
	}

	.results-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		border-bottom: 1px solid #eee;
		padding-bottom: 0.5rem;
		margin-bottom: 0.75rem;
	}
	.results-header h2 {
		font-size: 1rem;
		font-weight: 500;
		color: var(--text-secondary);
		margin: 0;
	}
	.results-text {
		font-size: 0.875rem;
		color: var(--md-on-surface);
	}
	.icon-button {
		background: none;
		border: none;
		border-radius: 50%;
		cursor: pointer;
		color: var(--text-secondary);
		padding: 0.25rem;
	}
	.icon-button:hover {
		color: var(--md-primary);
	}
</style>
