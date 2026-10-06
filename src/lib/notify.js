// Optional Telegram message to the owner (new sign-ups, redeemed codes). Never throws:
// a notification problem must not break the request that triggered it.
export async function notifyOwner(env, text) {
  try {
    const { results } = await env.DB.prepare("SELECT key, value FROM settings WHERE key IN ('telegram_token', 'telegram_chat_id')").all();
    const m = Object.fromEntries(results.map((r) => [r.key, r.value]));
    if (!m.telegram_token || !m.telegram_chat_id) return false;
    const res = await fetch(`https://api.telegram.org/bot${m.telegram_token}/sendMessage`, {
      method: 'POST', headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ chat_id: m.telegram_chat_id, text }),
      signal: AbortSignal.timeout(3000),
    });
    return res.ok;
  } catch { return false; }
}
