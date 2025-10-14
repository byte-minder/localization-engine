<script lang="ts">
	import { onMount } from 'svelte';
	import { theme } from '$lib/stores';
	import Header from '$lib/components/Header.svelte';
	import '../app.css';

	onMount(() => {
		const applyTheme = (currentTheme: string) => {
			const root = document.documentElement;
			const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

			if (currentTheme === 'dark' || (currentTheme === 'system' && isDark)) {
				root.classList.add('dark');
			} else {
				root.classList.remove('dark');
			}
		};

		const unsubscribe = theme.subscribe(applyTheme);

		const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
		const handleSystemChange = () => {
			if ($theme === 'system') {
				applyTheme('system');
			}
		};
		mediaQuery.addEventListener('change', handleSystemChange);
		
		return () => {
			unsubscribe();
			mediaQuery.removeEventListener('change', handleSystemChange);
		};
	});
</script>

<div class="app-container">
	<Header />
	<main>
		<slot />
	</main>
</div>

<style>
	.app-container {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
	}
	main {
		flex-grow: 1;
		padding: 2rem;
		max-width: 1200px;
		margin: 0 auto;
		width: 100%;
	}
</style>