<script lang="ts">
	import { get } from 'svelte/store';
	import { theme } from '$lib/stores';

	function cycleTheme() {
	
		const current = get(theme);
		const newTheme =
			current === 'light'
				? 'dark'
				: current === 'dark'
				? 'system'
				: 'light';
		theme.set(newTheme);
	}

</script>

<button on:click={cycleTheme} class="theme-toggle" title="Cycle Theme">
	{#if $theme === 'light'}
		<span>☀️ Light</span>
	{:else if $theme === 'dark'}
		<span>🌙 Dark</span>
	{:else}
		<span>💻 System</span>
	{/if}
</button>

<style>
	.theme-toggle {
		background-color: var(--surface);
		color: var(--text-secondary);
		border: 1px solid var(--border);
		border-radius: 20px;
		padding: 6px 12px;
		cursor: pointer;
		font-size: 0.875rem;
		font-weight: 500;
		display: flex;
		align-items: center;
		gap: 8px;
		transition: background-color 0.2s, color 0.2s;
	}
	.theme-toggle:hover {
		background-color: var(--background);
		color: var(--text-primary);
	}
	
</style>
