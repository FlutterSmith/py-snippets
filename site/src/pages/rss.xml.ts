import rss from '@astrojs/rss';
import type { APIContext } from 'astro';

import { plain, site, snippets, snippetUrl } from '../lib/site';

export function GET(context: APIContext) {
  return rss({
    title: site.name,
    description: 'Python snippets that still pass.',
    site: context.site!,
    items: snippets.map((s) => ({
      title: s.title,
      description: plain(s.summary),
      link: snippetUrl(s.slug),
      pubDate: new Date(`${s.published.slice(0, 10)}T00:00:00Z`),
      categories: [s.category, ...s.tags],
    })),
  });
}
