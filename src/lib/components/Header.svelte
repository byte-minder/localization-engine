<script lang="ts">
	import Icon from '$lib/components/Icon.svelte';
	import ThemeToggle from '$lib/components/ThemeToggle.svelte'; // Import the new component
</script>

<header>
	<nav>
		<a href="/" class="logo">
			<Icon name="translate" />
			<h1>Content Localizer</h1>
		</a>
		<div class="nav-links">
			<ul>
				<li><a href="/">Localize</a></li>
				<li><a href="/vocabulary">Vocabulary</a></li>
				<li><a href="/settings">Settings</a></li>
				<li><a href="/help">Help</a></li>
			</ul>
			<ThemeToggle /> </div>
	</nav>
</header>

<style>
	header {
		background-color: var(--surface);
		border-bottom: 1px solid var(--border);
		padding: 0.5rem 2rem;
	}
	nav {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	.logo {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		text-decoration: none;
		color: var(--text-primary);
	}
	h1 {
		font-size: 1.5rem;
		font-weight: 600;
	}
	.nav-links { 
		display: flex;
		align-items: center;
		gap: 2rem;
	}
	ul {
		list-style: none;
		display: flex;
		gap: 2rem;
		margin: 0;
		padding: 0;
	}
	a {
		text-decoration: none;
		color: var(--text-secondary);
		font-weight: 500;
		transition: color 0.2s;
	}
	a:hover {
		color: var(--primary);
	}
</style>