<script lang="ts">
	import Icon from './Icon.svelte';
	export let textToRead: string;

	function handleReadAloud() {
		
		
		if ('speechSynthesis' in window && textToRead) {
			const utterance = new SpeechSynthesisUtterance(textToRead);
			window.speechSynthesis.cancel(); 
			window.speechSynthesis.speak(utterance);
		} else {
			alert('Text-to-speech is not supported in your browser or there is no text to read.');
		}
	}
</script>



<button class="icon-button" on:click={handleReadAloud} title="Read Aloud">
	<Icon name="volume" />
	<span>Read Aloud</span>
</button>



<style>
	.icon-button {
		background: none;
		border: 1px solid #ccc;
		border-radius: 4px;
		cursor: pointer;
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.5rem 1rem;
		font-size: 0.9rem;
	}
	.icon-button:hover {
		background-color: #f1f1f1;
	}
</style>