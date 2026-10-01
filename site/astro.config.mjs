// @ts-check
import { readFileSync } from 'node:fs';

import { unified } from '@astrojs/markdown-remark';
import { defineConfig } from 'astro/config';

import { rehypePanels, remarkSnippets } from './src/lib/markdown.mjs';

const base = process.env.SITE_BASE ?? '/py-snippets';
// Written by `npm run generate` (the Python CLI). The Markdown pipeline only
// needs the list of Python versions CI runs the doctests on.
const meta = JSON.parse(readFileSync(new URL('./src/generated/meta.json', import.meta.url), 'utf8'));

export default defineConfig({
  site: process.env.SITE_URL ?? 'https://fluttersmith.github.io',
  base,
  trailingSlash: 'always',
  markdown: {
    // Code blocks are highlighted by rehypePanels, which also draws the
    // annotated function panels and the REPL panels. Astro's own
    // highlighter stays out of the way.
    syntaxHighlight: false,
    processor: unified({
      remarkPlugins: [[remarkSnippets, { base }]],
      rehypePlugins: [[rehypePanels, { pythons: meta.pythons }]],
    }),
  },
  build: { format: 'directory' },
  devToolbar: { enabled: false },
});
