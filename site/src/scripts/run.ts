// The Run panel: edits the snippet and runs its doctests with Python's own
// doctest module, inside Pyodide, in a worker. This file is a separate chunk,
// fetched only when someone clicks "Run in your browser".

const $ = <T extends HTMLElement = HTMLElement>(s: string) => document.querySelector<T>(s);
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
const base = document.documentElement.dataset.base ?? '/';
const TIMEOUT_MS = 5000;

interface Result {
  source: string;
  want: string;
  ok: boolean;
  got: string;
}
interface Reply {
  type: string;
  id?: number;
  version?: string;
  message?: string;
  results?: Result[];
  error?: string;
}

let worker: Worker | null = null;
let ready: Promise<string> | null = null;
let version = '';
let wired = false;
let seq = 0;
let previous: boolean[] = [];

const el = {
  runner: () => $('#runner')!,
  code: () => $<HTMLTextAreaElement>('#run-code')!,
  examples: () => $<HTMLTextAreaElement>('#run-ex')!,
  out: () => $('#run-out')!,
  status: () => $('#run-status')!,
  progress: () => $('#run-progress')!,
  go: () => $<HTMLButtonElement>('#run-go')!,
};

function progress(text: string, state: '' | 'ready' | 'error' = '') {
  const p = el.progress();
  p.textContent = text;
  p.className = `run-progress ${state}`.trim();
}

function status(text: string, state: '' | 'pass' | 'fail' = '') {
  const s = el.status();
  s.textContent = text;
  s.className = `run-status ${state}`.trim();
}

function boot(): Promise<string> {
  if (ready) return ready;
  const runner = el.runner();
  const indexURL = `https://cdn.jsdelivr.net/pyodide/v${runner.dataset.pyodide}/full/`;
  const python = runner.dataset.pyodide?.startsWith('314.') ? '3.14' : '3';
  progress(`Loading Python ${python} in your browser (≈7 MB, cached after the first time)…`);
  el.go().disabled = true;
  worker = new Worker(`${base}run-worker.js`, { type: 'module' });
  ready = new Promise<string>((resolve, reject) => {
    const w = worker!;
    const onMessage = ({ data }: MessageEvent<Reply>) => {
      if (data.type === 'ready') {
        w.removeEventListener('message', onMessage);
        version = data.version ?? '';
        progress(`Python ${version} is running in this page. Edit either box; the examples re-run as you type.`, 'ready');
        el.go().disabled = false;
        resolve(version);
      } else if (data.type === 'failed') {
        w.removeEventListener('message', onMessage);
        reject(new Error(data.message));
      }
    };
    w.addEventListener('message', onMessage);
    w.addEventListener('error', (e) => reject(new Error(e.message || 'The Python worker failed to start.')), { once: true });
    w.postMessage({ type: 'init', indexURL });
  }).catch((err: Error) => {
    progress(`Couldn't load Python: ${err.message}. Check your connection and try again.`, 'error');
    status('');
    stop();
    el.go().disabled = false;
    throw err;
  });
  return ready;
}

function stop() {
  worker?.terminate();
  worker = null;
  ready = null;
}

function call(code: string, examples: string): Promise<Reply> {
  const id = ++seq;
  const w = worker!;
  return new Promise((resolve) => {
    const timer = window.setTimeout(() => {
      w.removeEventListener('message', onMessage);
      stop();
      resolve({ type: 'result', id, error: `Stopped after ${TIMEOUT_MS / 1000} seconds. Is there an endless loop?\n` });
    }, TIMEOUT_MS);
    const onMessage = ({ data }: MessageEvent<Reply>) => {
      if (data.type !== 'result' || data.id !== id) return;
      clearTimeout(timer);
      w.removeEventListener('message', onMessage);
      resolve(data);
    };
    w.addEventListener('message', onMessage);
    w.postMessage({ type: 'run', id, code, examples });
  });
}

const span = (cls: string, text: string) => {
  const s = document.createElement('span');
  s.className = cls;
  s.textContent = text;
  return s;
};

function outLines(text: string, cls: string, prefix?: string): HTMLElement[] {
  const lines = text.replace(/\n$/, '').split('\n');
  return lines.map((line, i) => {
    const s = span(cls, '');
    if (prefix) s.append(span('k', i ? ' '.repeat(prefix.length) : prefix));
    s.append(line || ' ');
    return s;
  });
}

function render(results: Result[]) {
  const out = el.out();
  const label = `Python ${version}`;
  const rows = results.map((r, i) => {
    const ex = document.createElement('span');
    ex.className = 'ex';
    const tick = document.createElement('span');
    tick.className = `tick${r.ok ? '' : ' bad'}`;
    tick.dataset.tip = r.ok ? `Passes on ${label}` : `Fails on ${label}`;
    tick.append(span('', r.ok ? '✓' : '✗'), span('visually-hidden', r.ok ? 'passes: ' : 'fails: '));
    tick.firstElementChild!.setAttribute('aria-hidden', 'true');
    // A tick flips with a 120ms scale-in when its result changes.
    if (!reduced && previous[i] !== r.ok) {
      tick.classList.add('pending');
      requestAnimationFrame(() => requestAnimationFrame(() => tick.classList.remove('pending')));
    }
    const body = document.createElement('span');
    body.className = 'exb';
    r.source
      .replace(/\n$/, '')
      .split('\n')
      .forEach((line, k) => {
        const sl = span('sl', '');
        sl.append(span('p', k ? '... ' : '>>> '), line);
        body.append(sl);
      });
    if (r.ok) {
      if (r.want) body.append(...outLines(r.want, 'out'));
    } else {
      body.append(...outLines(r.want || '(nothing)', 'out want', 'Expected: '));
      body.append(...outLines(r.got || '(nothing)', 'out bad', 'Got:      '));
    }
    ex.append(tick, body);
    return ex;
  });
  previous = results.map((r) => r.ok);
  out.replaceChildren(...rows);
}

let latest = 0;
async function run() {
  const mine = ++latest;
  const code = el.code().value;
  const examples = el.examples().value;
  let reply: Reply;
  try {
    await boot();
    status('Running…');
    reply = await call(code, examples);
  } catch {
    return;
  }
  if (mine !== latest) return;
  if (reply.error) {
    previous = [];
    el.out().replaceChildren(span('err', reply.error.replace(/\n$/, '')));
    status(`The code didn't run: ${reply.error.trim().split('\n').pop()}`, 'fail');
    return;
  }
  const results = reply.results ?? [];
  render(results);
  const passed = results.filter((r) => r.ok).length;
  if (!results.length) status('No examples to run. Add a line starting with >>>.', 'fail');
  else if (passed === results.length) status(`${passed} of ${results.length} examples pass on Python ${version}.`, 'pass');
  else status(`${results.length - passed} of ${results.length} examples fail on Python ${version}.`, 'fail');
}

function reset() {
  el.code().value = el.code().defaultValue;
  el.examples().value = el.examples().defaultValue;
  status('Reset to the original code and examples.');
  void run();
}

/** Tab indents; Escape then Tab leaves the editor, so the keyboard is never trapped. */
function editorKeys(area: HTMLTextAreaElement) {
  let escaped = false;
  area.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      void run();
      return;
    }
    if (e.key === 'Escape') {
      escaped = true;
      return;
    }
    if (e.key === 'Tab' && !escaped && !e.shiftKey && !e.altKey && !e.ctrlKey && !e.metaKey) {
      e.preventDefault();
      const { selectionStart: s, selectionEnd: end, value } = area;
      area.value = value.slice(0, s) + '    ' + value.slice(end);
      area.selectionStart = area.selectionEnd = s + 4;
      area.dispatchEvent(new Event('input'));
    }
    escaped = false;
  });
  let timer: number | undefined;
  area.addEventListener('input', () => {
    if (el.runner().hidden) return;
    clearTimeout(timer);
    timer = window.setTimeout(run, 500);
  });
}

export function openRunner() {
  const runner = el.runner();
  const button = $('#run-btn');
  if (!wired) {
    wired = true;
    const mac = /Mac|iPhone|iPad/.test(navigator.platform);
    runner.querySelectorAll('kbd.mod').forEach((k) => (k.textContent = mac ? '⌘' : 'Ctrl'));
    el.go().addEventListener('click', () => void run());
    $('#run-reset')?.addEventListener('click', reset);
    editorKeys(el.code());
    editorKeys(el.examples());
  }
  if (runner.hidden) {
    runner.hidden = false;
    button?.setAttribute('aria-expanded', 'true');
    runner.scrollIntoView({ block: 'nearest', behavior: reduced ? 'auto' : 'smooth' });
  }
  el.code().focus({ preventScroll: true });
  void run();
}
