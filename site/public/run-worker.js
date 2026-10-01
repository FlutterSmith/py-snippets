// Runs Python off the main thread, so a slow or endless loop in edited code
// can be stopped without freezing the page. Loaded only when someone clicks
// "Run in your browser".
let py = null;

async function init(indexURL) {
  const [{ loadPyodide }, harness] = await Promise.all([
    import(`${indexURL}pyodide.mjs`),
    fetch(new URL('run-harness.py', self.location.href)).then((r) => {
      if (!r.ok) throw new Error(`run-harness.py: HTTP ${r.status}`);
      return r.text();
    }),
  ]);
  py = await loadPyodide({ indexURL, stdout: () => {}, stderr: () => {} });
  py.runPython(harness);
  return py.runPython('import sys; sys.version.split()[0]');
}

self.onmessage = async ({ data }) => {
  if (data.type === 'init') {
    try {
      const version = await init(data.indexURL);
      self.postMessage({ type: 'ready', version });
    } catch (err) {
      self.postMessage({ type: 'failed', message: String(err?.message ?? err) });
    }
    return;
  }
  if (data.type === 'run') {
    try {
      const run = py.globals.get('run_snippet');
      const out = run(data.code, data.examples);
      run.destroy();
      self.postMessage({ type: 'result', id: data.id, ...JSON.parse(out) });
    } catch (err) {
      self.postMessage({ type: 'result', id: data.id, error: String(err?.message ?? err) });
    }
  }
};
