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

	const DEFAULTS = {
		displayLanguage: "English",
		textSize: 14,
		autoTranslate: false,
		autoSubtitles: false,
		autoSync: false,
		screenReader: false,
		speechNav: false,
		highContrast: false,
	};

	function addLanguage() {
		const lang = prompt("Add a language (e.g. Spanish)");
		if (lang) {
			const trimmed = lang.trim();
			if (trimmed && !languages.includes(trimmed)) {
				languages.push(trimmed);
			}
		}
	}

	function saveSettings() {
		// Replace with real save/dispatch logic as needed
		console.log("Settings saved", {
			displayLanguage,
			textSize,
			autoTranslate,
			autoSubtitles,
			autoSync,
			screenReader,
			speechNav,
			highContrast,
		});
		alert("Settings saved (demo)");
	}

	function resetDefaults() {
		displayLanguage = DEFAULTS.displayLanguage;
		textSize = DEFAULTS.textSize;
		autoTranslate = DEFAULTS.autoTranslate;
		autoSubtitles = DEFAULTS.autoSubtitles;
		autoSync = DEFAULTS.autoSync;
		screenReader = DEFAULTS.screenReader;
		speechNav = DEFAULTS.speechNav;
		highContrast = DEFAULTS.highContrast;
	}
</script>

<svelte:head>
	<title>Settings</title>
</svelte:head>

<header class="bg-indigo-600 text-white shadow-sm">
	<div class="max-w-4xl mx-auto px-4 py-4">
		<h1 class="text-lg font-semibold">Settings</h1>
	</div>
</header>

<main class="max-w-4xl mx-auto p-6 space-y-6">
	<!-- Language Preferences -->
	<section class="bg-white rounded-lg shadow-sm p-6">
		<div class="flex items-start justify-between gap-4">
			<div>
				<h2 class="text-lg font-medium text-gray-900">Language Preferences</h2>
				<p class="mt-1 text-sm text-gray-600">
					Choose your preferred display language.
				</p>

				<select
					bind:value={displayLanguage}
					class="mt-3 block w-full max-w-xs rounded-md border border-gray-300 px-3 py-2 bg-white text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
					aria-label="Select display language"
				>
					{#each languages as lang}
						<option value={lang}>{lang}</option>
					{/each}
				</select>
			</div>

			<div class="flex-shrink-0">
				<button
					on:click={addLanguage}
					class="inline-flex items-center gap-2 rounded-md bg-emerald-400 px-3 py-2 text-sm font-medium text-black hover:bg-emerald-300 focus:outline-none focus:ring-2 focus:ring-emerald-300"
				>
					+ Add Language
				</button>
			</div>
		</div>
	</section>

	<!-- Automation Preferences -->
	<section class="bg-white rounded-lg shadow-sm p-6">
		<h2 class="text-lg font-medium text-gray-900">Automation</h2>
		<p class="mt-1 text-sm text-gray-600">
			Enable automation features to streamline localization workflows.
		</p>

		<div class="mt-4 space-y-3">
			<label class="flex items-center gap-3">
				<input
					type="checkbox"
					bind:checked={autoTranslate}
					class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
				/>
				<span class="text-sm text-gray-800"
					>Auto-translate uploaded content</span
				>
			</label>

			<label class="flex items-center gap-3">
				<input
					type="checkbox"
					bind:checked={autoSubtitles}
					class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
				/>
				<span class="text-sm text-gray-800"
					>Auto-generate subtitles for multimedia</span
				>
			</label>

			<label class="flex items-center gap-3">
				<input
					type="checkbox"
					bind:checked={autoSync}
					class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
				/>
				<span class="text-sm text-gray-800"
					>Sync translations across formats</span
				>
			</label>
		</div>
	</section>

	<!-- Accessibility -->
	<section class="bg-white rounded-lg shadow-sm p-6">
		<h2 class="text-lg font-medium text-gray-900">Accessibility</h2>
		<p class="mt-1 text-sm text-gray-600">
			Adapt your learning experience for better accessibility.
		</p>

		<div class="mt-4 space-y-3">
			<label class="flex items-center gap-3">
				<input
					id="screenReader"
					type="checkbox"
					bind:checked={screenReader}
					class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
				/>
				<span class="text-sm text-gray-800">Enable Screen Reader</span>
			</label>

			<label class="flex items-center gap-3">
				<input
					id="speechNav"
					type="checkbox"
					bind:checked={speechNav}
					class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
				/>
				<span class="text-sm text-gray-800">Speech Navigation</span>
			</label>

			<label class="flex items-center gap-3">
				<input
					id="highContrast"
					type="checkbox"
					bind:checked={highContrast}
					class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
				/>
				<span class="text-sm text-gray-800">High Contrast Mode</span>
			</label>

			<div class="mt-3">
				<label for="text-size-slider" class="block text-sm text-gray-700"
					>Text Size: <span class="font-medium">{textSize}px</span></label
				>
				<input
					id="text-size-slider"
					type="range"
					min="12"
					max="24"
					step="1"
					bind:value={textSize}
					class="mt-2 w-full"
					aria-label="Text size slider"
				/>
			</div>
		</div>
	</section>

	<!-- Buttons -->
	<div class="flex justify-end gap-3">
		<button
			on:click={resetDefaults}
			class="rounded-md bg-gray-100 px-4 py-2 text-sm font-medium text-gray-800 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-200"
		>
			Reset Defaults
		</button>

		<button
			on:click={saveSettings}
			class="rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-300"
		>
			Save Changes
		</button>
	</div>
</main>
