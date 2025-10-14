<script lang="ts">
	import Icon from "$lib/components/Icon.svelte";
	import ThemeToggle from "$lib/components/ThemeToggle.svelte";
</script>

<header class="bg-white border-b border-gray-200 px-8 py-2">
	<nav class="flex justify-between items-center">
		<a
			href="/"
			class="flex items-center gap-3 no-underline text-gray-900 hover:text-indigo-600 transition-colors"
		>
			<Icon name="translate" />
			<h1 class="text-2xl font-semibold">Content Localizer</h1>
		</a>
		<div class="flex items-center gap-8">
			<ul class="list-none flex gap-8 m-0 p-0">
				<li>
					<a
						href="/"
						class="no-underline text-gray-600 font-medium hover:text-indigo-600 transition-colors"
					>
						Localize
					</a>
				</li>
				<li>
					<a
						href="/vocabulary"
						class="no-underline text-gray-600 font-medium hover:text-indigo-600 transition-colors"
					>
						Vocabulary
					</a>
				</li>
				<li>
					<a
						href="/settings"
						class="no-underline text-gray-600 font-medium hover:text-indigo-600 transition-colors"
					>
						Settings
					</a>
				</li>
				<li>
					<a
						href="/help"
						class="no-underline text-gray-600 font-medium hover:text-indigo-600 transition-colors"
					>
						Help
					</a>
				</li>
			</ul>
			<ThemeToggle />
		</div>
	</nav>
</header>
