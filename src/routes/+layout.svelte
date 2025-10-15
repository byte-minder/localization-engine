<script lang="ts">
	import { onMount } from "svelte";
	import { theme } from "$lib/stores";
	import Header from "$lib/components/Header.svelte";
	import "../app.css";

	onMount(() => {
		const applyTheme = (currentTheme: string) => {
			const root = document.documentElement;
			const isDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

			if (currentTheme === "dark" || (currentTheme === "system" && isDark)) {
				root.classList.add("dark");
			} else {
				root.classList.remove("dark");
			}
		};

		applyTheme($theme);

		const unsubscribe = theme.subscribe(applyTheme);

		const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
		const handleSystemChange = () => {
			if ($theme === "system") {
				applyTheme("system");
			}
		};

		mediaQuery.addEventListener("change", handleSystemChange);

		return () => {
			unsubscribe();
			mediaQuery.removeEventListener("change", handleSystemChange);
		};
	});
</script>

<div class="flex flex-col min-h-screen">
	<Header />
	<main class="flex-1 w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
		<slot />
	</main>
</div>
