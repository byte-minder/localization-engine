import { writable } from 'svelte/store';
import { browser } from '$app/environment';

export const skillDomains = writable<string[]>([]);

export type Theme = 'light' | 'dark' | 'system';

function getInitialTheme(): Theme {
	if (browser) {
		const stored = localStorage.getItem('theme');
		if (stored === 'light' || stored === 'dark' || stored === 'system') {
			return stored;
		}
	}
	return 'system';
}

export const theme = writable<Theme>(getInitialTheme());

if (browser) {
	theme.subscribe((value) => {
		localStorage.setItem('theme', value);
	});
}
