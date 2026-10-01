// All client-side behaviour. Every feature is progressive: the pages are
// complete without this script. The Run panel lives in ./run.ts and is only
// fetched when someone asks for it.

const $ = <T extends Element = HTMLElement>(s: string, r: ParentNode = document) => r.querySelector<T>(s);
const $$ = <T extends Element = HTMLElement>(s: string, r: ParentNode = document) => [...r.querySelectorAll<T>(s)];
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
const base = document.documentElement.dataset.base ?? '/';

function store(key: string, value?: string): string | null {
  try {
    if (value === undefined) return localStorage.getItem(key);
    localStorage.setItem(key, value);
  } catch {
    // Storage can be blocked (private mode); the feature still works per page.
  }
  return null;
}

/* ---------- toast ---------- */
let toastTimer: number | undefined;
function toast(message: string) {
  const el = $('#toast');
  if (!el) return;
  el.textContent = message;
  el.classList.add('on');
  clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => el.classList.remove('on'), 2600);
}

/* ---------- theme: System → Light → Dark ---------- */
const THEMES = ['system', 'light', 'dark'] as const;
type Theme = (typeof THEMES)[number];
function applyTheme(theme: Theme) {
  const root = document.documentElement;
  if (theme === 'system') root.removeAttribute('data-theme');
  else root.setAttribute('data-theme', theme);
  const label = $('#theme-label');
  if (label) label.textContent = theme[0].toUpperCase() + theme.slice(1);
  $('#theme')?.setAttribute('aria-label', `Theme: ${theme}. Change theme`);
}
function cycleTheme() {
  const current = (store('ps-theme') as Theme | null) ?? 'system';
  const next = THEMES[(THEMES.indexOf(current) + 1) % THEMES.length];
  store('ps-theme', next);
  applyTheme(next);
}

/* ---------- annotated code panels ---------- */
interface Note {
  line: number;
  text: string;
}

// Seeded jitter keeps arrows hand-drawn but identical between renders.
function rng(seed: number) {
  let s = seed % 2147483647 || 1;
  return () => (s = (s * 16807) % 2147483647) / 2147483647;
}

function arrowPaths(x0: number, y0: number, x1: number, y1: number, seed: number): [string, string] {
  const r = rng(seed * 97 + 13);
  const cx = (x0 + x1) / 2;
  const cy = Math.min(y0, y1) - 24 - Math.abs(y0 - y1) * 0.2;
  const pts: [number, number][] = [];
  for (let i = 0; i <= 18; i++) {
    const t = i / 18;
    const u = 1 - t;
    const w = Math.sin(Math.PI * t) * 1.3;
    pts.push([u * u * x0 + 2 * u * t * cx + t * t * x1 + (r() - 0.5) * w, u * u * y0 + 2 * u * t * cy + t * t * y1 + (r() - 0.5) * w]);
  }
  const d = pts.map(([x, y], i) => `${i ? 'L' : 'M'}${x.toFixed(1)} ${y.toFixed(1)}`).join(' ');
  const [ax, ay] = pts[pts.length - 3];
  const ang = Math.atan2(y1 - ay, x1 - ax);
  const head = (a: number) => `${(x1 - 9 * Math.cos(ang + a)).toFixed(1)} ${(y1 - 9 * Math.sin(ang + a)).toFixed(1)}`;
  return [d, `M${head(0.5)} L${x1.toFixed(1)} ${y1.toFixed(1)} L${head(-0.5)}`];
}

/** Notes keep inline `code` as mono; the rest is handwriting. */
function noteNodes(text: string): Node[] {
  return text.split('`').map((part, i) => {
    if (!(i % 2)) return document.createTextNode(part);
    const code = document.createElement('code');
    code.textContent = part;
    return code;
  });
}

function layoutPanel(panel: HTMLElement, animate: boolean) {
  const notes: Note[] = JSON.parse(panel.dataset.notes ?? '[]');
  const wide = panel.clientWidth >= 620 && notes.length > 0;
  panel.classList.toggle('lane-on', wide);
  panel.classList.toggle('compact', panel.clientWidth < 620);
  const svg = $<SVGSVGElement>('svg.arrows', panel);
  const lane = $('.lane', panel);
  if (!svg || !lane) return;
  svg.replaceChildren();
  if (!wide) return;

  if (lane.childElementCount !== notes.length) {
    lane.replaceChildren(
      ...notes.map((n, i) => {
        const div = document.createElement('div');
        div.className = 'note';
        div.dataset.n = String(i);
        div.append(...noteNodes(n.text));
        div.addEventListener('mouseenter', () => focusNote(panel, i, true));
        div.addEventListener('mouseleave', () => focusNote(panel, i, false));
        return div;
      }),
    );
  }

  const lines = $$('pre.code .line', panel);
  const body = $('.panel-body', panel)!.getBoundingClientRect();
  const laneBox = lane.getBoundingClientRect();
  let lastBottom = -Infinity;
  const seedBase = [...(panel.dataset.notes ?? '')].reduce((a, c) => a + c.charCodeAt(0), 0);

  $$('.note', lane).forEach((note, i) => {
    const line = lines[notes[i].line];
    if (!line) return;
    const lr = line.getBoundingClientRect();
    const range = document.createRange();
    range.selectNodeContents(line);
    const textRight = Math.max(...[...range.getClientRects()].map((r) => r.right), lr.left + 60);
    let top = lr.top + lr.height / 2 - body.top - 11;
    top = Math.max(top, lastBottom + 10);
    note.style.top = `${top}px`;
    lastBottom = top + note.offsetHeight;

    const x0 = laneBox.left - body.left + 10;
    const y0 = top + 12;
    const x1 = Math.min(textRight - body.left + 12, laneBox.left - body.left - 26);
    const y1 = lr.top + lr.height / 2 - body.top;
    arrowPaths(x0, y0, x1, y1, seedBase + i).forEach((d, k) => {
      const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      path.setAttribute('d', d);
      path.setAttribute('pathLength', '1');
      path.dataset.n = String(i);
      if (animate && !reduced) {
        path.style.strokeDasharray = '1';
        path.style.strokeDashoffset = '1';
        path.style.transitionDelay = `${i * 140 + k * 360}ms`;
        requestAnimationFrame(() => requestAnimationFrame(() => (path.style.strokeDashoffset = '0')));
      }
      svg.appendChild(path);
    });
  });
}

function focusNote(panel: HTMLElement, n: number, on: boolean) {
  const notes: Note[] = JSON.parse(panel.dataset.notes ?? '[]');
  $$('pre.code .line', panel)[notes[n]?.line]?.classList.toggle('hl', on);
  $$(`svg.arrows path[data-n="${n}"]`, panel).forEach((p) => p.classList.toggle('on', on));
  $(`.notes-list li[data-n="${n}"]`, panel)?.classList.toggle('on', on);
}

function panelText(panel: HTMLElement) {
  if (panel.dataset.raw !== undefined) return panel.dataset.raw;
  return $$('pre.code .line', panel)
    .map((line) => {
      const clone = line.cloneNode(true) as HTMLElement;
      clone.querySelectorAll('.mk').forEach((m) => m.remove());
      return clone.textContent ?? '';
    })
    .join('\n');
}

async function copyText(value: string, button: HTMLElement, select?: Element | null) {
  const label = $('span', button) ?? button;
  const original = label.textContent;
  try {
    await navigator.clipboard.writeText(value);
    label.textContent = 'Copied';
  } catch {
    if (select) {
      const range = document.createRange();
      range.selectNodeContents(select);
      const sel = getSelection();
      sel?.removeAllRanges();
      sel?.addRange(range);
    }
    label.textContent = 'Selected';
  }
  setTimeout(() => (label.textContent = original), 1400);
}

function initPanels(root: ParentNode = document) {
  const observer = new ResizeObserver((entries) => {
    for (const e of entries) layoutPanel(e.target as HTMLElement, false);
  });
  for (const panel of $$('.panel-code', root)) {
    if (panel.dataset.ready) continue;
    panel.dataset.ready = '1';
    const r = panel.getBoundingClientRect();
    const visible = r.top < innerHeight && r.bottom > 0 && panel.offsetParent !== null;
    layoutPanel(panel, visible);
    observer.observe(panel);
    $$('.mk', panel).forEach((m) =>
      m.addEventListener('click', () => {
        const n = Number(m.dataset.n);
        focusNote(panel, n, true);
        setTimeout(() => focusNote(panel, n, false), 1800);
      }),
    );
  }
  for (const panel of $$('.panel-repl', root)) panel.classList.toggle('compact', panel.clientWidth < 420);
}

/* ---------- home: the hero session types itself (once, ≈900ms) ---------- */
function truncate(line: HTMLElement, html: string, chars: number, caret: boolean) {
  line.innerHTML = html;
  const walker = document.createTreeWalker(line, NodeFilter.SHOW_TEXT);
  let left = chars;
  for (let node = walker.nextNode() as Text | null; node; node = walker.nextNode() as Text | null) {
    if (node.parentElement?.classList.contains('p')) continue;
    if (left >= node.data.length) left -= node.data.length;
    else {
      node.data = node.data.slice(0, left);
      left = 0;
    }
  }
  if (caret) line.insertAdjacentHTML('beforeend', '<span class="caret" aria-hidden="true"></span>');
}

function heroSession() {
  const box = $('.hero-repl[data-anim]');
  if (!box) return;
  if (reduced) {
    box.removeAttribute('data-anim');
    return;
  }
  const items = $$('.ex', box).map((ex) => {
    const lines = $$('.sl', ex).map((el) => ({ el, html: el.innerHTML, len: (el.textContent ?? '').length - 4 }));
    return { ex, tick: $('.tick', ex)!, lines, outs: $$('.out', ex), chars: lines.reduce((n, l) => n + l.len, 0) };
  });
  for (const it of items) {
    it.ex.hidden = true;
    it.tick.classList.add('pending');
    it.outs.forEach((o) => (o.hidden = true));
  }
  box.removeAttribute('data-anim');

  // Per example: type (300ms), print (+40ms), tick lands (+40ms, 120ms scale-in), pause.
  const TYPE = 300;
  const STEP = TYPE + 160;
  const start = performance.now();
  const frame = (now: number) => {
    const t = now - start;
    let done = true;
    items.forEach((it, i) => {
      const local = t - i * STEP;
      if (local < 0) {
        done = false;
        return;
      }
      it.ex.hidden = false;
      const typed = Math.min(it.chars, Math.round((local / TYPE) * it.chars));
      let left = typed;
      const counts = it.lines.map((l) => {
        const n = Math.min(left, l.len);
        left -= n;
        return n;
      });
      const at = counts.reduce((last, n, k) => (k === 0 || n > 0 ? k : last), 0);
      it.lines.forEach((l, k) => {
        l.el.hidden = k > at;
        if (k <= at) truncate(l.el, l.html, counts[k], typed < it.chars && k === at);
      });
      it.outs.forEach((o) => (o.hidden = local < TYPE + 40));
      if (local >= TYPE + 80) it.tick.classList.remove('pending');
      else done = false;
    });
    if (!done) requestAnimationFrame(frame);
  };
  requestAnimationFrame(frame);
}

/* ---------- random snippet ---------- */
function randomSnippet() {
  const slugs: string[] = JSON.parse($('#snip-slugs')?.textContent ?? '[]');
  if (!slugs.length) return;
  const current = document.documentElement.dataset.slug;
  const pool = slugs.filter((s) => s !== current);
  location.href = `${base}s/${pool[Math.floor(Math.random() * pool.length)]}/`;
}

/* ---------- search (Pagefind) ---------- */
interface PagefindResult {
  data: () => Promise<{ url: string; excerpt: string; meta: Record<string, string> }>;
}
interface Pagefind {
  search: (q: string) => Promise<{ results: PagefindResult[] }>;
}
let pagefind: Pagefind | null | undefined;
async function loadPagefind(): Promise<Pagefind | null> {
  if (pagefind !== undefined) return pagefind;
  try {
    const path = `${base}pagefind/pagefind.js`;
    pagefind = (await import(/* @vite-ignore */ path)) as Pagefind;
  } catch {
    pagefind = null;
  }
  return pagefind;
}

const escapeHtml = (s: string) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]!);

let selected = 0;
let searchSeq = 0;
async function runSearch() {
  const input = $<HTMLInputElement>('#q')!;
  const list = $('#results')!;
  const term = input.value.trim();
  const seq = ++searchSeq;
  if (!term) {
    list.innerHTML = '<li class="empty">Type a function name, an idea or a stdlib call like <code class="i">batched</code>.</li>';
    return;
  }
  const pf = await loadPagefind();
  if (!pf) {
    list.innerHTML = '<li class="empty">Search runs on the built site. Run <code class="i">npm run build</code> and preview it.</li>';
    return;
  }
  const { results } = await pf.search(term);
  const data = await Promise.all(results.slice(0, 8).map((r) => r.data()));
  if (seq !== searchSeq) return;
  selected = 0;
  if (!data.length) {
    list.innerHTML = `<li class="empty">Nothing for “${escapeHtml(term)}”. Try a function name like <code class="i">group_by</code>.</li>`;
    return;
  }
  list.innerHTML = data
    .map(
      (d, i) =>
        `<li><a href="${d.url}" class="${i === 0 ? 'sel' : ''}"><span class="n">${escapeHtml(d.meta.pkg ?? '')}</span>` +
        `<span class="t">${escapeHtml(d.meta.title ?? '')}</span><span class="c">${d.excerpt}</span></a></li>`,
    )
    .join('');
}

let lastFocus: HTMLElement | null = null;
function openSearch() {
  const bg = $('#pal')!;
  lastFocus = document.activeElement as HTMLElement | null;
  bg.hidden = false;
  const input = $<HTMLInputElement>('#q')!;
  input.value = '';
  void runSearch();
  input.focus();
  void loadPagefind();
}
function closeDialog(id: string) {
  const el = $(id);
  if (!el || el.hidden) return false;
  el.hidden = true;
  lastFocus?.focus();
  return true;
}
function openHelp() {
  lastFocus = document.activeElement as HTMLElement | null;
  $('#help')!.hidden = false;
  $<HTMLButtonElement>('#help button')?.focus();
}

/* ---------- Run (lazy) ---------- */
function openRun() {
  if (!$('#run-btn')) return;
  void import('./run').then((m) => m.openRunner());
}

/* ---------- boot ---------- */
function boot() {
  applyTheme((store('ps-theme') as Theme | null) ?? 'system');
  $('#theme')?.addEventListener('click', cycleTheme);
  $('#open-search')?.addEventListener('click', openSearch);
  $$('[data-random]').forEach((b) => b.addEventListener('click', randomSnippet));
  $('#run-btn')?.addEventListener('click', openRun);

  document.addEventListener('click', (e) => {
    const target = e.target as HTMLElement;
    const copy = target.closest<HTMLElement>('[data-copy]');
    if (copy) {
      const panel = copy.closest<HTMLElement>('.panel')!;
      void copyText(panelText(panel), copy, $('pre', panel));
    }
    const line = target.closest<HTMLElement>('[data-copy-text]');
    if (line) void copyText(line.dataset.copyText ?? '', line, $('#import-line'));
    if (target.closest('[data-open-search]')) {
      e.preventDefault();
      openSearch();
    }
    if (target.id === 'pal' || target.closest('#results a')) closeDialog('#pal');
    if (target.id === 'help' || target.closest('[data-close-help]')) closeDialog('#help');
  });

  let debounce: number | undefined;
  $('#q')?.addEventListener('input', () => {
    clearTimeout(debounce);
    debounce = window.setTimeout(runSearch, 120);
  });
  $('#q')?.addEventListener('keydown', (e) => {
    const items = $$<HTMLAnchorElement>('#results a');
    if ((e.key === 'ArrowDown' || e.key === 'ArrowUp') && items.length) {
      e.preventDefault();
      items[selected]?.classList.remove('sel');
      selected = (selected + (e.key === 'ArrowDown' ? 1 : items.length - 1)) % items.length;
      items[selected].classList.add('sel');
      items[selected].scrollIntoView({ block: 'nearest' });
    } else if (e.key === 'Enter' && items[selected]) {
      location.href = items[selected].href;
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && (closeDialog('#pal') || closeDialog('#help'))) return;
    // Keep Tab inside an open dialog.
    if (e.key === 'Tab') {
      const dialog = $$('.pal-bg').find((d) => !d.hidden);
      if (dialog) {
        const items = $$<HTMLElement>('input, button, a[href]', dialog);
        const i = items.indexOf(document.activeElement as HTMLElement);
        if (e.shiftKey && i <= 0) {
          e.preventDefault();
          items[items.length - 1].focus();
        } else if (!e.shiftKey && i === items.length - 1) {
          e.preventDefault();
          items[0].focus();
        }
      }
      return;
    }
    const t = e.target as HTMLElement;
    if (t.closest('input, textarea, select, [contenteditable]') || e.metaKey || e.ctrlKey || e.altKey) return;
    if ($$('.pal-bg').some((d) => !d.hidden)) return;
    const link = (rel: string) => $<HTMLAnchorElement>(`a[data-rel="${rel}"]`);
    switch (e.key) {
      case '/':
        e.preventDefault();
        openSearch();
        break;
      case 'r':
        randomSnippet();
        break;
      case 't':
        cycleTheme();
        break;
      case 'e':
        if ($('#run-btn')) {
          e.preventDefault();
          openRun();
        }
        break;
      case 'c': {
        const btn = $<HTMLElement>('main .panel-code [data-copy]');
        if (btn) {
          void copyText(panelText(btn.closest('.panel')!), btn);
          toast('Copied the function.');
        }
        break;
      }
      case '?':
        openHelp();
        break;
      case 'ArrowLeft':
        if (link('prev')) location.href = link('prev')!.href;
        break;
      case 'ArrowRight':
        if (link('next')) location.href = link('next')!.href;
        break;
    }
  });

  const progress = $('#progress');
  if (progress && document.documentElement.dataset.slug) {
    addEventListener(
      'scroll',
      () => {
        const h = document.documentElement.scrollHeight - innerHeight;
        progress.style.width = `${h > 0 ? (scrollY / h) * 100 : 0}%`;
      },
      { passive: true },
    );
  }

  heroSession();
  initPanels();
  document.fonts?.ready.then(() => $$('.panel.lane-on').forEach((p) => layoutPanel(p, false)));
}

boot();
