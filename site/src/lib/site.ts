import meta from '../generated/meta.json';
import { versionsFrom } from './versions.mjs';

export interface Link {
  name: string;
  url: string;
}

export interface Fn {
  name: string;
  signature: string;
  summary: string;
}

export interface Example {
  source: string;
  want: string;
}

export interface SnippetMeta {
  slug: string;
  title: string;
  summary: string;
  category: string;
  tags: string[];
  since: string;
  complexity: string;
  stdlib: string | null;
  fixes: string | null;
  published: string;
  module: string;
  import: string;
  functions: Fn[];
  code: string;
  examples: Example[];
  origin: null | { upstream: Link[]; change: string; kind: string };
  related: string[];
  previous: string | null;
  next: string | null;
}

export interface Category {
  id: string;
  label: string;
  blurb: string;
  count: number;
}

export interface StdlibRow {
  id: string;
  instead: string;
  use: string;
  since: string;
  note?: string;
  example: string;
  upstream: Link[];
}

export interface IdiomRow {
  id: string;
  group: string;
  js: string;
  python: string;
  note?: string;
  example: string;
  upstream: Link[];
}

export const site = {
  name: 'fluttersmith/py-snippets',
  repo: 'https://github.com/FlutterSmith/py-snippets',
  attribution: 'https://github.com/FlutterSmith/py-snippets/blob/main/ATTRIBUTION.md',
  upstreamRepo: meta.upstream.repo as string,
  upstreamTotal: meta.upstream.total as number,
  version: meta.version as string,
  verifiedAt: meta.verifiedAt as string,
  pythons: meta.pythons as string[],
  ccby: 'https://creativecommons.org/licenses/by/4.0/',
};

/** Pyodide release the Run panel loads, and the Python it ships. */
export const pyodide = { version: '314.0.7', python: '3.14' };

/** All published snippets, in catalog order. */
export const snippets: SnippetMeta[] = (meta.snippets as SnippetMeta[]).filter((s) => s.published);
export const categories: Category[] = (meta.categories as Category[]).filter((c) => c.count > 0);
export const tags = meta.tags as Record<string, string>;
export const stdlibRows = meta.stdlib as StdlibRow[];
export const idiomRows = meta.idioms as IdiomRow[];
export const exampleCount = snippets.reduce((n, s) => n + s.examples.length, 0);

const bySlug = new Map(snippets.map((s) => [s.slug, s]));
export const snippet = (slug: string) => bySlug.get(slug);
export const categoryLabel = (id: string) => categories.find((c) => c.id === id)?.label ?? id;

export const versions = (since?: string): string[] => versionsFrom(since, site.pythons);
export const first = site.pythons[0];
export const last = site.pythons[site.pythons.length - 1];
/** "3.11–3.14" */
export const rangeShort = (since?: string) => {
  const v = versions(since);
  return v.length > 1 ? `${v[0]}–${v[v.length - 1]}` : v[0];
};

/** Joins a path onto the configured base, keeping the trailing slash style. */
export function url(path = ''): string {
  const base = import.meta.env.BASE_URL.replace(/\/?$/, '/');
  return base + path.replace(/^\//, '');
}

export const snippetUrl = (slug: string) => url(`s/${slug}/`);
export const pkg = (s: SnippetMeta) => `pysnippets.${s.category}`;

/** Parameter names from a signature: `f(a: int, *, b=1) -> x` gives `a, *, b`. */
export function args(signature: string): string {
  const open = signature.indexOf('(');
  let depth = 0;
  let close = -1;
  for (let i = open; i < signature.length; i++) {
    const c = signature[i];
    if ('([{'.includes(c)) depth++;
    else if (')]}'.includes(c) && --depth === 0) {
      close = i;
      break;
    }
  }
  const inner = signature.slice(open + 1, close);
  const parts: string[] = [];
  let cur = '';
  depth = 0;
  for (const c of inner) {
    if ('([{'.includes(c)) depth++;
    if (')]}'.includes(c)) depth--;
    if (c === ',' && depth === 0) {
      parts.push(cur);
      cur = '';
    } else cur += c;
  }
  if (cur.trim()) parts.push(cur);
  return parts.map((p) => p.split(/[:=]/)[0].trim()).join(', ');
}

const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

/**
 * Renders the small amount of inline Markdown used in meta strings:
 * `code`, **bold**, *emphasis* and [links](url). Everything else is text.
 */
export function md(source: string | null | undefined): string {
  if (!source) return '';
  return source
    .split(/(`[^`]+`)/)
    .map((part) => {
      if (part.startsWith('`') && part.endsWith('`') && part.length > 1) return `<code class="i">${esc(part.slice(1, -1))}</code>`;
      return esc(part)
        .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
        .replace(/(^|[^*\w])\*([^*\s][^*]*)\*/g, '$1<em>$2</em>')
        .replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (_, label, href) => `<a href="${href}">${label}</a>`);
    })
    .join('');
}

/** Plain text, for meta descriptions and RSS. */
export const plain = (source: string) => source.replace(/[`*]/g, '');

export function formatDate(iso: string): string {
  if (!iso) return '';
  return new Date(`${iso.slice(0, 10)}T00:00:00Z`).toLocaleDateString('en-GB', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    timeZone: 'UTC',
  });
}
