// Builds the site's two signature components as hast:
// - the annotated function panel (Python code with `# @note` margin notes)
// - the REPL panel (a doctest session with a tick per passing example)
// Used by the Markdown pipeline and by pages that render code directly, so
// both produce identical markup.
import { createHighlighter } from 'shiki';

/** Syntax colours for the dark panel (the same in light and dark mode). */
const theme = {
  name: 'ps-panel',
  type: 'dark',
  colors: { 'editor.background': '#00000000', 'editor.foreground': '#E2EBE5' },
  tokenColors: [
    { settings: { foreground: '#E2EBE5' } },
    { scope: ['comment', 'punctuation.definition.comment'], settings: { foreground: '#7F9288', fontStyle: 'italic' } },
    {
      scope: [
        'keyword',
        'storage',
        'storage.type',
        'storage.modifier',
        'keyword.control',
        'keyword.operator.logical',
        'keyword.operator.new',
        'constant.language',
        'variable.language',
      ],
      settings: { foreground: '#7FD0E6' },
    },
    { scope: ['keyword.operator', 'punctuation'], settings: { foreground: '#B4C3BA' } },
    {
      scope: [
        'support.function.builtin',
        'support.type',
        'support.class',
        'entity.name.type',
        'entity.name.class',
        'support.type.exception',
        'entity.name.function.decorator',
        'meta.function.decorator',
      ],
      settings: { foreground: '#C9B6FF' },
    },
    {
      scope: ['string', 'string.quoted', 'string.interpolated', 'punctuation.definition.string', 'storage.type.string'],
      settings: { foreground: '#A8DCA0' },
    },
    { scope: ['constant.character.format.placeholder', 'meta.fstring punctuation.definition'], settings: { foreground: '#E2EBE5' } },
    { scope: ['string.regexp', 'constant.character.escape'], settings: { foreground: '#A8DCA0' } },
    { scope: ['constant.numeric', 'constant.character'], settings: { foreground: '#FFB98F' } },
  ],
};

let highlighterPromise;
function highlighter() {
  highlighterPromise ??= createHighlighter({ themes: [theme], langs: ['python'] });
  return highlighterPromise;
}

const NOTE_LINE = /^\s*#\s*@note\s+(.+?)\s*$/;
const NOTE_TRAILING = /^(.*?\S)\s*#\s*@note\s+(.+?)\s*$/;

/**
 * Removes `# @note` comments from [code]. A comment on its own line
 * annotates the next line; a trailing one annotates its own line.
 * @param {string} code
 */
export function extractNotes(code) {
  const out = [];
  const notes = [];
  let pending = [];
  for (const raw of code.replace(/\n$/, '').split('\n')) {
    const own = raw.match(NOTE_LINE);
    if (own) {
      pending.push(own[1]);
      continue;
    }
    const trailing = raw.match(NOTE_TRAILING);
    out.push(trailing ? trailing[1] : raw);
    const line = out.length - 1;
    for (const text of pending) notes.push({ line, text });
    if (trailing) notes.push({ line, text: trailing[2] });
    pending = [];
  }
  return { code: out.join('\n'), notes };
}

/** Parses `key="value"` pairs from a fence's info string. */
export function parseMeta(meta = '') {
  const attrs = {};
  for (const m of meta.matchAll(/(\w+)="([^"]*)"/g)) attrs[m[1]] = m[2];
  return attrs;
}

/**
 * Splits a `>>>` session into doctest examples, the way doctest reads it:
 * `>>> ` starts an example, `... ` continues its source, and every other
 * line up to the next prompt is the expected output.
 * @param {string} text
 * @returns {{ source: string, want: string }[]}
 */
export function parsePycon(text) {
  const examples = [];
  let current = null;
  for (const line of text.replace(/\n$/, '').split('\n')) {
    if (/^>>>( |$)/.test(line)) {
      current = { source: `${line.slice(4)}\n`, want: '', open: true };
      examples.push(current);
    } else if (current?.open && /^\.\.\.( |$)/.test(line)) {
      current.source += `${line.slice(4)}\n`;
    } else if (current) {
      current.open = false;
      if (line.trim() || current.want) current.want += `${line}\n`;
    }
  }
  return examples.map(({ source, want }) => ({ source, want: want.replace(/\n+$/, want.trim() ? '\n' : '') }));
}

/** Turns examples back into session text. */
export function toPycon(examples) {
  return examples
    .map(({ source, want }) => {
      const lines = source.replace(/\n$/, '').split('\n');
      return lines.map((l, i) => `${i ? '...' : '>>>'} ${l}`.trimEnd()).join('\n') + '\n' + want;
    })
    .join('');
}

export const el = (tagName, properties = {}, children = []) => ({ type: 'element', tagName, properties, children });
export const text = (value) => ({ type: 'text', value });

const COPY_ICON = el('svg', { viewBox: '0 0 16 16', ariaHidden: 'true', className: ['icon-copy'] }, [
  el('rect', { x: 5, y: 5, width: 9, height: 9, rx: 1, fill: 'none', stroke: 'currentColor', strokeWidth: 1.4 }),
  el('path', { d: 'M3 11V3a1 1 0 0 1 1-1h7', fill: 'none', stroke: 'currentColor', strokeWidth: 1.4 }),
]);

const copyButton = () =>
  el('button', { type: 'button', className: ['copy'], dataCopy: '' }, [COPY_ICON, el('span', {}, [text('Copy')])]);

/** Inline `code` inside a note becomes a mono span; the rest stays handwritten. */
export function noteChildren(note) {
  return note.split('`').map((part, i) => (i % 2 ? el('code', {}, [text(part)]) : text(part)));
}

async function highlightLines(code) {
  const hl = await highlighter();
  const root = hl.codeToHast(code, { lang: 'python', theme: 'ps-panel' });
  const pre = root.children.find((c) => c.type === 'element' && c.tagName === 'pre');
  const codeEl = pre.children.find((c) => c.type === 'element' && c.tagName === 'code');
  return codeEl.children.filter((c) => c.type === 'element');
}

/** The "3.11 to 3.14" range a snippet is checked on. */
export function rangeLabel(range) {
  if (!range?.length) return '';
  return range.length === 1 ? range[0] : `${range[0]} to ${range[range.length - 1]}`;
}

/**
 * The annotated function panel.
 * @param {{ code: string, meta?: string }} input
 * @returns {Promise<import('hast').Element>}
 */
export async function buildPanel({ code, meta = '' }) {
  const attrs = parseMeta(meta);
  const { code: clean, notes } = extractNotes(code);
  const lines = await highlightLines(clean);
  lines.forEach((node, i) => {
    notes.forEach((n, k) => {
      if (n.line !== i) return;
      node.children.push(
        el('button', { type: 'button', className: ['mk'], dataN: k, ariaLabel: `Note ${k + 1}: ${n.text.replaceAll('`', '')}` }, [
          text(String(k + 1)),
        ]),
      );
    });
  });
  const pre = el('pre', { className: ['code'], tabIndex: 0, ariaLabel: attrs.file ? `Code: ${attrs.file}` : 'Code' }, [
    el('code', {}, lines.flatMap((l, i) => (i ? [text('\n'), l] : [l]))),
  ]);

  const head = [el('span', { className: ['file'] }, [text(attrs.file ?? 'python')])];
  if (attrs.file) {
    head.push(
      el('span', { className: ['ok'], title: 'Linted with ruff and type-checked with mypy --strict in CI' }, [
        text('✓'),
        el('span', { className: ['okt'] }, [text(' ruff · mypy --strict')]),
      ]),
    );
  }

  const children = [
    el('div', { className: ['panel-head'], dataPagefindIgnore: '' }, [...head, el('span', { className: ['spacer'] }), copyButton()]),
    el('div', { className: ['panel-body'] }, [
      pre,
      el('div', { className: ['lane'], ariaHidden: 'true' }),
      el('svg', { className: ['arrows'], ariaHidden: 'true' }),
    ]),
  ];
  if (notes.length) {
    children.push(
      el(
        'ol',
        { className: ['notes-list'], ariaLabel: 'Notes' },
        notes.map((n, i) => el('li', { dataN: i, dataLine: n.line }, noteChildren(n.text))),
      ),
    );
  }
  return el(
    'figure',
    { className: ['panel', 'panel-code'], dataNotes: notes.length ? JSON.stringify(notes) : undefined, dataKind: attrs.file ? 'code' : 'plain' },
    children,
  );
}

function outputLines(want, cls = 'out') {
  if (!want) return [];
  const lines = want.replace(/\n$/, '').split('\n');
  const tb = lines[0]?.startsWith('Traceback (most recent call last)');
  return lines.map((line, i) => {
    const classes = [cls];
    if (tb && (i === 0 || line.trim() === '...')) classes.push('dim');
    else if (tb && i === lines.length - 1) classes.push('exc');
    return el('span', { className: classes }, [text(line || ' ')]);
  });
}

/**
 * The REPL panel: a doctest session with a tick per example.
 * @param {{ code: string, range?: string[], label?: string, foot?: import('hast').Element[] }} input
 * @returns {Promise<import('hast').Element>}
 */
export async function buildRepl({ code, range = [], label = 'examples', foot }) {
  const examples = parsePycon(code);
  const passed = range.length ? `Passed on Python ${rangeLabel(range)}` : 'Passes in CI';
  const allSource = examples.map((e) => e.source.replace(/\n$/, '')).join('\n');
  const lines = await highlightLines(allSource);
  let at = 0;
  const rows = examples.map((ex) => {
    const n = ex.source.replace(/\n$/, '').split('\n').length;
    const src = lines.slice(at, at + n).map((line, i) =>
      el('span', { className: ['sl'] }, [el('span', { className: ['p'] }, [text(i ? '... ' : '>>> ')]), ...line.children]),
    );
    at += n;
    return el('span', { className: ['ex'] }, [
      el('span', { className: ['tick'], dataTip: passed }, [
        el('span', { ariaHidden: 'true' }, [text('✓')]),
        el('span', { className: ['visually-hidden'] }, [text(`${passed.replace(/^Passed/, 'passed')}: `)]),
      ]),
      el('span', { className: ['exb'] }, [...src, ...outputLines(ex.want)]),
    ]);
  });

  const children = [
    el('div', { className: ['panel-head'], dataPagefindIgnore: '' }, [
      el('span', { className: ['file'] }, [text(label)]),
      el('span', { className: ['ok'], title: `Every example is a doctest. ${passed}.` }, [
        text('✓'),
        el('span', { className: ['okt'] }, [text(` ${examples.length} doctest${examples.length === 1 ? '' : 's'}${range.length ? ` · ${rangeLabel(range).replace(' to ', '–')}` : ''}`)]),
      ]),
      el('span', { className: ['spacer'] }),
      copyButton(),
    ]),
    el('pre', { className: ['repl'], tabIndex: 0, ariaLabel: 'Example session' }, [el('code', {}, rows)]),
  ];
  if (foot) children.push(el('div', { className: ['panel-foot'] }, foot));
  return el('figure', { className: ['panel', 'panel-repl'], dataKind: 'repl', dataRaw: code.replace(/\n$/, '') }, children);
}

/**
 * A light, compact session for the ledger pages: prompts, output and a tick.
 * No syntax colours: it sits on paper, not on the dark panel.
 * @param {{ code: string, range?: string[] }} input
 */
export function buildProof({ code, range = [] }) {
  const examples = parsePycon(code);
  const passed = range.length ? `Passed on Python ${rangeLabel(range)}` : 'Passes in CI';
  return el(
    'pre',
    { className: ['proof'], ariaLabel: 'Proof' },
    examples.map((ex) =>
      el('span', { className: ['ex'] }, [
        el('span', { className: ['tick'], dataTip: ex.want ? passed : undefined }, [
          // Setup lines (imports, assignments) pass too, but a tick on each is noise.
          ...(ex.want
            ? [el('span', { ariaHidden: 'true' }, [text('✓')]), el('span', { className: ['visually-hidden'] }, [text(`${passed.replace(/^Passed/, 'passed')}: `)])]
            : []),
        ]),
        el('span', { className: ['exb'] }, [
          ...ex.source
            .replace(/\n$/, '')
            .split('\n')
            .map((l, i) => el('span', { className: ['sl'] }, [el('span', { className: ['p'] }, [text(i ? '... ' : '>>> ')]), text(l)])),
          ...outputLines(ex.want),
        ]),
      ]),
    ),
  );
}
