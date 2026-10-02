// PIN/password hashing and random id/key helpers (Web Crypto only — no npm deps).

function bytesToHex(bytes) {
  return [...bytes].map((b) => b.toString(16).padStart(2, '0')).join('');
}

async function sha256Hex(input) {
  const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(input));
  return bytesToHex(new Uint8Array(digest));
}

// Salted with the record's own id/username plus a server-side secret, so neither
// a leaked DB alone nor a leaked secret alone is enough to recover PINs/passwords.
export async function hashSecretValue(value, salt, serverSecret) {
  return sha256Hex(`${serverSecret}:${salt}:${value}`);
}

export async function verifySecretValue(value, salt, serverSecret, expectedHash) {
  const actual = await hashSecretValue(value, salt, serverSecret);
  return timingSafeEqual(actual, expectedHash);
}

export function timingSafeEqual(a, b) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

// A short numeric PIN is easy for a student to retype on a phone keyboard.
export function randomPin(digits = 4) {
  const max = 10 ** digits;
  const n = crypto.getRandomValues(new Uint32Array(1))[0] % max;
  return String(n).padStart(digits, '0');
}

export function randomKey() {
  return crypto.randomUUID().replace(/-/g, '');
}
