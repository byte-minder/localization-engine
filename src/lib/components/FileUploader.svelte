<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import Icon from './Icon.svelte';

	let fileInput: HTMLInputElement;
	let active = false;
	const dispatch = createEventDispatcher();

	function handleFileSelect(files: FileList | null) {
		if (files && files.length > 0) {
			dispatch('fileSelected', files[0]);
		}
		active = false;
	}
</script>


<div
	class="dropzone"
	class:active
	on:dragenter|preventDefault|stopPropagation={() => (active = true)}
	on:dragleave|preventDefault|stopPropagation={() => (active = false)}
	on:dragover|preventDefault|stopPropagation
	on:drop|preventDefault|stopPropagation={(e) => handleFileSelect(e.dataTransfer?.files ?? null)}
	on:click={() => fileInput.click()}
	on:keydown={(e) => e.key === 'Enter' && fileInput.click()}
	role="button"
	tabindex="0"
>
	<Icon name="upload" />
	<p>
		<strong>Click to upload</strong> or drag and drop your content.
	</p>
	<small>Supports Text, PDF, MP3, WAV, OGG</small>
	<input
		type="file"
		bind:this={fileInput}
		on:change={(e) => handleFileSelect((e.currentTarget as HTMLInputElement).files)}
		accept=".txt,.pdf,.mp3,.wav,.ogg"
		hidden
	/>
</div>



<style>
	.dropzone {
		border: 2px dashed #adb5bd;
		border-radius: 8px;
		padding: 2rem;
		text-align: center;
		cursor: pointer;
		transition: background-color 0.2s, border-color 0.2s;
	}
	.dropzone:hover,
	.dropzone.active {
		background-color: #e9ecef;
		border-color: #007bff;
	}
	p {
		margin: 0.5rem 0;
	}
	small {
		color: #6c757d;
	}
</style>