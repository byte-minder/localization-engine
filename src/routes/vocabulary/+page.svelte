<!-- Generated Using AI  -->
<script>
	let activeTab = "wordlist";
	let selectedSector = "Healthcare";
	let selectedLanguage = "English";
	let searchQuery = "";

	const sectors = ["Healthcare", "Construction", "IT", "Agriculture", "Hospitality"];
	const languages = ["English", "Hindi", "Telugu"];
</script>

<!-- Top App Bar -->
<header class="app-bar">
	<h1>Vocabulary Bank</h1>
</header>

<main class="container">
	<!-- Filters -->
	<section class="filters">
		<div class="filter-group">
			<label for="sector-select">Sector:</label>
			<select id="sector-select" bind:value={selectedSector}>
				{#each sectors as sector}
					<option value={sector}>{sector}</option>
				{/each}
			</select>
		</div>

		<div class="filter-group">
			<label for="language-select">Language:</label>
			<select id="language-select" bind:value={selectedLanguage}>
				{#each languages as lang}
					<option value={lang}>{lang}</option>
				{/each}
			</select>
			<button class="add-lang-btn">+ Add Language</button>
		</div>

		<input
			type="text"
			placeholder="Search for a word..."
			bind:value={searchQuery}
			class="search-bar"
		/>
	</section>

	<!-- Tabs -->
	<nav class="tabs">
		<button class:active={activeTab === "wordlist"} on:click={() => (activeTab = "wordlist")}>
			Word List
		</button>
		<button class:active={activeTab === "examples"} on:click={() => (activeTab = "examples")}>
			Usage Examples
		</button>
		<button class:active={activeTab === "audio"} on:click={() => (activeTab = "audio")}>
			Audio Practice
		</button>
	</nav>

	<!-- Tab Panels -->
	<section class="tab-content">
		{#if activeTab === "wordlist"}
			<div class="card-grid">
				<div class="card">
					<h3>Welding</h3>
					<p>Translation: वेल्डिंग (Hindi)</p>
					<button>🔊 Play</button>
				</div>
				<div class="card">
					<h3>Safety Gear</h3>
					<p>Translation: सुरक्षा उपकरण (Hindi)</p>
					<button>🔊 Play</button>
				</div>
			</div>
		{:else if activeTab === "examples"}
			<div class="examples">
				<div class="card">
					<p><strong>Word:</strong> Safety Gear</p>
					<p>“Always wear safety gear before operating heavy machinery.”</p>
					<p><em>“भारी मशीन चलाने से पहले हमेशा सुरक्षा उपकरण पहनें।”</em></p>
				</div>
			</div>
		{:else if activeTab === "audio"}
			<div class="audio-practice">
				<div class="upload-box">Upload Audio (MP3, WAV, OGG)</div>
				<div class="audio-buttons">
					<button>Upload</button>
					<button>Play</button>
					<button>Record New</button>
				</div>
			</div>
		{/if}
	</section>
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
		padding: 1rem 2rem;
	}

	.filters {
		display: flex;
		flex-wrap: wrap;
		gap: 1rem;
		align-items: center;
		margin-bottom: 1rem;
	}

	.filter-group {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	select,
	input {
		padding: 0.5rem;
		border-radius: 8px;
		border: 1px solid #ccc;
	}

	.add-lang-btn {
		background: #03dac6;
		color: black;
		border: none;
		padding: 0.5rem 1rem;
		border-radius: 8px;
		cursor: pointer;
	}

	.tabs {
		display: flex;
		gap: 1rem;
		border-bottom: 2px solid #e0e0e0;
		margin-bottom: 1rem;
	}

	.tabs button {
		background: none;
		border: none;
		padding: 0.75rem 1rem;
		cursor: pointer;
		font-weight: 500;
		color: #666;
	}

	.tabs button.active {
		color: #6200ee;
		border-bottom: 2px solid #6200ee;
	}

	.card-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
		gap: 1rem;
	}

	.card {
		background: #fff;
		padding: 1rem;
		border-radius: 12px;
		box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
	}

	.audio-practice {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1rem;
	}

	.upload-box {
		border: 2px dashed #ccc;
		padding: 2rem;
		width: 100%;
		text-align: center;
		border-radius: 12px;
		color: #888;
	}
</style>
