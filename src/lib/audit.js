export async function audit(env, teacher, action, detail = '') {
  try {
    await env.DB.prepare('INSERT INTO audit_log (teacher_id, action, detail) VALUES (?1, ?2, ?3)')
      .bind(teacher ? teacher.id : null, action, String(detail).slice(0, 500)).run();
  } catch { /* logging must never break the request */ }
}
