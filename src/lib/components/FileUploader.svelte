<script lang="ts">
	import { createEventDispatcher } from "svelte";
	import Icon from "./Icon.svelte";

	let fileInput: HTMLInputElement;
	let active = false;
	const dispatch = createEventDispatcher();

	function handleFileSelect(files: FileList | null) {
		if (files && files.length > 0) {
			dispatch("fileSelected", files[0]);
		}
		active = false;
	}
</script>

<div
	class={`mx-auto max-w-xl flex flex-col items-center gap-3 p-8 rounded-lg border-2 border-dashed border-gray-400 text-center cursor-pointer transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-300 ${
		active
			? "bg-gray-100 border-blue-500"
			: "hover:bg-gray-100 hover:border-blue-500"
	}`}
	on:dragenter|preventDefault|stopPropagation={() => (active = true)}
	on:dragleave|preventDefault|stopPropagation={() => (active = false)}
	on:dragover|preventDefault|stopPropagation
	on:drop|preventDefault|stopPropagation={(e) =>
		handleFileSelect(e.dataTransfer?.files ?? null)}
	on:click={() => fileInput.click()}
	on:keydown={(e) => {
		if (e.key === "Enter" || e.key === " ") {
			e.preventDefault();
			fileInput.click();
		}
	}}
	role="button"
	tabindex="0"
	aria-label="Click or press Enter/Space to upload a file, or drag and drop"
>
	<!-- Icon: adjust size via tailwind classes passed down to the Icon component -->
	<Icon name="upload" />

	<p class="text-sm text-gray-700">
		<strong class="font-semibold">Click to upload</strong>
		<span class="block">or drag and drop your content.</span>
	</p>

	<small class="text-xs text-gray-500">Supports Text, PDF, MP3, WAV, OGG</small>

	<input
		type="file"
		bind:this={fileInput}
		on:change={(e) =>
			handleFileSelect((e.currentTarget as HTMLInputElement).files)}
		accept=".txt,.pdf,.mp3,.wav,.ogg"
		class="hidden"
	/>
</div>
