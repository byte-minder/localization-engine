<script lang="ts">
	import { get } from "svelte/store";
	import { theme } from "$lib/stores";

	function cycleTheme() {
		const current = get(theme);
		const newTheme =
			current === "light" ? "dark" : current === "dark" ? "system" : "light";
		theme.set(newTheme);
	}
</script>

<button
	on:click={cycleTheme}
	class="bg-white text-gray-600 border border-gray-300 rounded-full px-3 py-1.5 cursor-pointer text-sm font-medium flex items-center gap-2 transition-colors hover:bg-gray-50 hover:text-gray-900"
	title="Cycle Theme"
>
	{#if $theme === "light"}
		<span>☀️ Light</span>
	{:else if $theme === "dark"}
		<span>🌙 Dark</span>
	{:else}
		<span> System</span>
	{/if}
</button>
