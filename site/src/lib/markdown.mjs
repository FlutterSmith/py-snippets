// Remark/rehype plugins that turn a snippet page's GitHub-friendly Markdown
// into the site's markup.
import path from 'node:path';

import { visit } from 'unist-util-visit';

import { buildPanel, buildRepl, el } from './panel.mjs';
import { versionsFrom } from './versions.mjs';

const REPO_BLOB = 'https://github.com/FlutterSmith/py-snippets/blob/main';
const MARKER = /^<\?snippet\s+"([^"]+)"(?:\s+part="([\w-]+)")?\s*\?>/;

/**
 * - moves `<?snippet "lists/x.py"?>` markers onto the following fence as
 *   `file="x.py"` (and `part="examples"` for the doctest session)
 * - drops HTML comments
 * - rewrites links between snippets to site routes, other relative links to GitHub
 * @param {{ base: string }} options
 */
export function remarkSnippets({ base }) {
  const root = base.endsWith('/') ? base : `${base}/`;
  return (tree, file) => {
    const children = tree.children;
    for (let i = children.length - 1; i >= 0; i--) {
      const node = children[i];
      if (node.type !== 'html') continue;
      const marker = node.value.match(MARKER);
      const next = children[i + 1];
      if (marker && next?.type === 'code') {
        const part = marker[2] ? ` part="${marker[2]}"` : '';
        next.meta = `${next.meta ?? ''} file="${path.posix.basename(marker[1])}" module="${marker[1]}"${part}`.trim();
      }
      if (marker || node.value.trimStart().startsWith('<!--')) children.splice(i, 1);
    }

    const slug = path.basename(path.dirname(file.path ?? file.history?.[0] ?? ''));
    visit(tree, ['link', 'definition'], (node) => {
      const url = node.url;
      if (!url || /^[a-z]+:/i.test(url) || url.startsWith('#')) return;
      const other = url.match(/^\.\.\/([a-z0-9-]+)\/(?:index\.md)?(#.*)?$/);
      if (other) {
        node.url = `${root}s/${other[1]}/${other[2] ?? ''}`;
        return;
      }
      node.url = `${REPO_BLOB}/${path.posix.normalize(`content/snippets/${slug}/${url}`)}`;
    });
  };
}

/**
 * Replaces every `pre > code` with a panel: `python` fences become the
 * annotated function panel, `pycon` fences the REPL panel. A slot for the
 * Run button goes right after the doctest session.
 * @param {{ pythons?: string[] }} [options]
 */
export function rehypePanels({ pythons = [] } = {}) {
  return async (tree, file) => {
    const since = file.data?.astro?.frontmatter?.since;
    const range = versionsFrom(since, pythons);
    const jobs = [];
    const slots = [];
    visit(tree, 'element', (node, index, parent) => {
      if (node.tagName !== 'pre' || !parent) return;
      const code = node.children.find((c) => c.type === 'element' && c.tagName === 'code');
      if (!code) return;
      const lang = (code.properties?.className ?? []).find((c) => String(c).startsWith('language-'))?.slice(9) ?? 'text';
      const source = code.children.map((c) => (c.type === 'text' ? c.value : '')).join('');
      const meta = code.data?.meta ?? '';
      const job =
        lang === 'pycon'
          ? buildRepl({ code: source, range }).then((panel) => {
              parent.children[index] = panel;
              if (/part="examples"/.test(meta)) slots.push({ parent, panel });
            })
          : buildPanel({ code: source, meta }).then((panel) => {
              parent.children[index] = panel;
            });
      jobs.push(job);
      return 'skip';
    });
    await Promise.all(jobs);
    for (const { parent, panel } of slots) {
      parent.children.splice(parent.children.indexOf(panel) + 1, 0, el('div', { dataRunSlot: '' }));
    }
  };
}
