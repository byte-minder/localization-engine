<script lang="ts">
	import Icon from "./Icon.svelte";
	export let textToRead: string;

	function handleReadAloud() {
		if ("speechSynthesis" in window && textToRead) {
			const utterance = new SpeechSynthesisUtterance(textToRead);
			window.speechSynthesis.cancel();
			window.speechSynthesis.speak(utterance);
		} else {
			alert(
				"Text-to-speech is not supported in your browser or there is no text to read.",
			);
		}
	}
</script>

<button
	class="bg-transparent border border-gray-300 rounded cursor-pointer inline-flex items-center gap-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
	on:click={handleReadAloud}
	title="Read Aloud"
>
	<Icon name="volume" />
	<span>Read Aloud</span>
</button>
