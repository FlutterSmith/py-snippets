import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

// The Python CLI (`snip validate`) is the real gatekeeper for frontmatter.
// This schema only types the fields the pages read.
const snippets = defineCollection({
  loader: glob({
    pattern: '*/index.md',
    base: '../content/snippets',
    generateId: ({ entry }) => entry.split('/')[0],
  }),
  schema: z.looseObject({
    slug: z.string(),
    title: z.string(),
    summary: z.string(),
  }),
});

export const collections = { snippets };
