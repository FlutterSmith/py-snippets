/**
 * Python versions from `since` upward, e.g. ["3.11", "3.12", "3.13", "3.14"].
 * @param {string | undefined} since
 * @param {string[]} pythons
 */
export function versionsFrom(since, pythons) {
  const key = (v) => v.split('.').map(Number).reduce((a, n) => a * 1000 + n, 0);
  return pythons.filter((v) => key(v) >= key(since ?? pythons[0]));
}
