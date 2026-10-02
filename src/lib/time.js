// Server is the only source of truth for whether a test session is open —
// a student's phone clock must never be trusted for this.
export function sessionWindow(session) {
  const start = Date.parse(session.scheduled_start);
  const end = start + session.duration_minutes * 60000;
  const now = Date.now();
  let phase;
  if (session.status === 'closed') phase = 'closed';
  else if (now < start) phase = 'upcoming';
  else if (now < end) phase = 'open';
  else phase = 'closed';
  return { start, end, now, phase };
}
