const PREFIX = "bit101.school.";
const RESULT_PREFIX = "result:";
const MAX_RESULTS = 10;
const MAX_RESULT_CHARS = 2_000_000;

export const schoolSessionKey = `${PREFIX}session`;

export interface SchoolCacheEntry<T> {
  data: T;
  cachedAt: number;
}

function fullKey(key: string): string {
  return `${PREFIX}${key}`;
}

export function resultKey(kind: string, ...parts: (string | boolean)[]): string {
  return `${RESULT_PREFIX}${kind}:${parts.map((part) => encodeURIComponent(String(part))).join(":")}`;
}

export function readSchoolCache<T>(key: string): SchoolCacheEntry<T> | null {
  try {
    const raw = localStorage.getItem(fullKey(key));
    if (!raw) return null;
    const entry = JSON.parse(raw);
    if (!entry || typeof entry !== "object" || Array.isArray(entry) ||
      !Number.isFinite(entry.cachedAt) || !("data" in entry)) return null;
    return entry as SchoolCacheEntry<T>;
  } catch {
    return null;
  }
}

export function writeSchoolCache<T>(key: string, data: T): boolean {
  try {
    const serialized = JSON.stringify(data);
    if (!serialized) return false;
    if (key.startsWith(RESULT_PREFIX)) {
      if (serialized.length > MAX_RESULT_CHARS) return false;
      pruneResults(fullKey(key));
    }
    const entry: SchoolCacheEntry<T> = {
      data,
      cachedAt: Math.floor(Date.now() / 1000),
    };
    localStorage.setItem(fullKey(key), JSON.stringify(entry));
    return true;
  } catch {
    return false;
  }
}

function pruneResults(keepKey: string) {
  const prefix = `${PREFIX}${RESULT_PREFIX}`;
  const entries: { key: string; cachedAt: number }[] = [];
  for (let index = 0; index < localStorage.length; index++) {
    const key = localStorage.key(index);
    if (!key?.startsWith(prefix) || key === keepKey) continue;
    let cachedAt = 0;
    try {
      cachedAt = Number(JSON.parse(localStorage.getItem(key) || "{}").cachedAt) || 0;
    } catch {
      cachedAt = 0;
    }
    entries.push({ key, cachedAt });
  }
  entries.sort((a, b) => a.cachedAt - b.cachedAt);
  for (const entry of entries.slice(0, Math.max(0, entries.length - MAX_RESULTS + 1))) {
    localStorage.removeItem(entry.key);
  }
}

export function removeSchoolCache(key: string) {
  try {
    localStorage.removeItem(fullKey(key));
  } catch {
    return;
  }
}

export function clearSchoolResults(kind: string, sid: string) {
  const prefix = fullKey(`${RESULT_PREFIX}${kind}:${encodeURIComponent(sid)}`);
  try {
    const keys: string[] = [];
    for (let index = 0; index < localStorage.length; index++) {
      const key = localStorage.key(index);
      if (key === prefix || key?.startsWith(`${prefix}:`)) keys.push(key);
    }
    keys.forEach((key) => localStorage.removeItem(key));
  } catch {
    return;
  }
}
