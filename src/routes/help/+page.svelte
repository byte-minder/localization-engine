<script lang="ts">
	import { slide } from 'svelte/transition';
// generated with AI, for backend engineer if need any improvement pls do
	// Add an 'open' state to each FAQ item
	let faqs = [
		{
			q: 'File upload fails or gets stuck.',
			a: 'Ensure your file is one of the supported formats (TXT, PDF, MP3, WAV, OGG) and does not exceed the maximum size limit (e.g., 50MB). Check your internet connection.',
			open: false
		},
		{
			q: 'Why is the translation inaccurate?',
			a: 'Translation quality depends on the selected domain vocabulary. For highly technical content, ensure you have selected the correct domain. If terms are still incorrect, add them to the Vocabulary Bank.',
			open: false
		},
		{
			q: 'The "Read Aloud" feature is not working.',
			a: 'This accessibility feature relies on your browser\'s built-in text-to-speech capabilities. Ensure you are using a modern browser like Chrome, Firefox, or Edge. Also, check that your device\'s sound is on and working.',
			open: false
		},
		{
			q: 'How do I add support for a new language?',
			a: 'Adding a new language requires backend model training and configuration. Please contact the system administrator to integrate a new language model into the platform.',
			open: false
		}
	];

	function toggleFaq(index: number) {
		// Simple toggle for each item
		// faqs[index].open = !faqs[index].open;

		// --- OR ---

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

<section>
	<h2>Troubleshooting & FAQ</h2>
	<p>Find solutions to common issues and answers to frequently asked questions.</p>

	<div class="faq-list">
		{#each faqs as faq, i}
			<div class="faq-item" class:open={faq.open}>
				<button class="faq-question" on:click={() => toggleFaq(i)}>
					<span>{faq.q}</span>
					<span class="icon"></span>
				</button>
				{#if faq.open}
					<div class="faq-answer" transition:slide={{ duration: 250 }}>
						<p>{faq.a}</p>
					</div>
				{/if}
			</div>
		{/each}
	</div>
</section>

<style>
	section {
		max-width: 800px;
	}
	.faq-list {
		margin-top: 2rem;
	}
	.faq-item {
		border: 1px solid #e0e0e0;
		border-radius: 4px;
		margin-bottom: 1rem;
		overflow: hidden; /* Important for animation */
	}
	.faq-question {
		display: flex;
		justify-content: space-between;
		align-items: center;
		width: 100%;
		text-align: left;
		background: none;
		border: none;
		padding: 1rem;
		font-weight: 600;
		cursor: pointer;
		font-size: 1rem;
	}
	.faq-answer {
		padding: 0 1rem 1rem 1rem;
	}
	.faq-answer p {
		margin: 0;
		line-height: 1.6;
	}
	/* Simple chevron icon for open/close state */
	.icon {
		border: solid #333;
		border-width: 0 2px 2px 0;
		display: inline-block;
		padding: 3px;
		transform: rotate(45deg);
		transition: transform 0.2s ease-in-out;
	}
	.faq-item.open .icon {
		transform: rotate(-135deg);
	}
</style>