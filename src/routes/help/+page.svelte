<script lang="ts">
	import { slide } from "svelte/transition";

	// for backend engineer if need any improvement pls do
	// Add an 'open' state to each FAQ item
	let faqs = [
		{
			q: "File upload fails or gets stuck.",
			a: "Ensure your file is one of the supported formats (TXT, PDF, MP3, WAV, OGG) and does not exceed the maximum size limit (e.g., 50MB). Check your internet connection.",
			open: false,
		},
		{
			q: "Why is the translation inaccurate?",
			a: "Translation quality depends on the selected domain vocabulary. For highly technical content, ensure you have selected the correct domain. If terms are still incorrect, add them to the Vocabulary Bank.",
			open: false,
		},
		{
			q: 'The "Read Aloud" feature is not working.',
			a: "This accessibility feature relies on your browser's built-in text-to-speech capabilities. Ensure you are using a modern browser like Chrome, Firefox, or Edge. Also, check that your device's sound is on and working.",
			open: false,
		},
		{
			q: "How do I add support for a new language?",
			a: "Adding a new language requires backend model training and configuration. Please contact the system administrator to integrate a new language model into the platform.",
			open: false,
		},
	];

	function toggleFaq(index: number) {
		// Accordion-style: close others when one opens
		faqs = faqs.map((faq, i) => {
			if (i === index) {
				return { ...faq, open: !faq.open };
			}
			return { ...faq, open: false };
		});
	}
</script>

<svelte:head>
	<title>Help & Troubleshooting</title>
</svelte:head>

<section class="mx-auto max-w-2xl px-4 py-8">
	<header class="mb-4">
		<h2 class="text-2xl font-semibold text-gray-900">Troubleshooting & FAQ</h2>
		<p class="mt-2 text-sm text-gray-600">
			Find solutions to common issues and answers to frequently asked questions.
		</p>
	</header>

	<div class="mt-6 space-y-4">
		{#each faqs as faq, i}
			<div
				class="rounded-lg border border-gray-200 overflow-hidden"
				class:open={faq.open}
			>
				<button
					class="w-full flex items-center justify-between px-4 py-3 text-left text-base font-medium focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-300 hover:bg-gray-50 transition"
					on:click={() => toggleFaq(i)}
					aria-expanded={faq.open}
				>
					<span class="text-gray-800">{faq.q}</span>
					<!-- Chevron (rotates when open) -->
					<svg
						class="w-4 h-4 transform transition-transform duration-200"
						class:rotate-180={faq.open}
						viewBox="0 0 20 20"
						fill="none"
						aria-hidden="true"
					>
						<path
							d="M6 8l4 4 4-4"
							stroke="currentColor"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
					</svg>
				</button>

				{#if faq.open}
					<div
						class="px-4 pb-4 pt-0 bg-white"
						transition:slide={{ duration: 250 }}
					>
						<p class="text-sm text-gray-700 leading-relaxed">{faq.a}</p>
					</div>
				{/if}
			</div>
		{/each}
	</div>
</section>
