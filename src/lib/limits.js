// Fixed-window rate limiter backed by D1. Returns true when the call is allowed.
export async function allow(env, key, max, windowSeconds) {
  const now = Math.floor(Date.now() / 1000);
  const row = await env.DB.prepare('SELECT count, window_start FROM rate_limits WHERE key = ?1').bind(key).first();
  if (!row || now - row.window_start >= windowSeconds) {
    await env.DB.prepare(
      'INSERT INTO rate_limits (key, count, window_start) VALUES (?1, 1, ?2) ON CONFLICT(key) DO UPDATE SET count = 1, window_start = ?2',
    ).bind(key, now).run();
    return true;
  }
  if (row.count >= max) return false;
  await env.DB.prepare('UPDATE rate_limits SET count = count + 1 WHERE key = ?1').bind(key).run();
  return true;
}

export function clientIp(req) {
  return req.headers.get('CF-Connecting-IP') || req.headers.get('X-Forwarded-For') || 'local';
}
