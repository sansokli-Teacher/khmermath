// Fair turns for the card game: the teams open the cards one after another, so questions + bonus boxes must divide by the number of teams.
// Same rule as planCards() in public/js/teamgame.js (the game applies it again when it starts, so both always agree).
export function planCards(Q, S, n, poolMax) {
  const keep = { Q, S, T: Q + S, per: n > 0 ? (Q + S) / n : Q + S, changed: false, short: n > 1 && Q + S < n };
  if (n <= 1 || Q + S < n) return keep;
  const rem = (Q + S) % n;
  if (rem === 0) return keep;
  const add = n - rem;
  let nq = Q, ns = S;
  if (Q + add <= poolMax && add <= rem) nq = Q + add;                          // 1. add the missing questions from the lessons' spare questions
  else if (S > 0 && S + add <= 12 && add <= rem) ns = S + add;                 // 2. no spare questions: add bonus boxes (when bonus boxes are on)
  else { let cut = rem; const fromQ = Math.min(cut, Math.max(0, nq - 1)); nq -= fromQ; cut -= fromQ; ns -= Math.min(ns, cut); }   // 3. take the surplus away, questions first so the bonus stays
  if (nq < 1 || (nq + ns) % n !== 0 || nq + ns < n) {                          // fallback: only questions, a multiple of n
    nq = Math.floor(Math.min(Q + S, Math.max(poolMax, 0)) / n) * n; ns = 0;
    if (nq < n) return keep;
  }
  return { Q: nq, S: ns, T: nq + ns, per: (nq + ns) / n, changed: true, short: false };
}
