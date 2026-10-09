// Exam Khmer — Worker entry point. Plain fetch handler, no router library,
// matching the style of /counter/src/index.js on khmermath.org's Cloudflare account.
import { err } from './lib/http.js';
import * as teacher from './api/teacher.js';
import * as classes from './api/classes.js';
import * as tests from './api/tests.js';
import * as images from './api/images.js';
import * as sessions from './api/sessions.js';
import * as student from './api/student.js';
import * as year from './api/year.js';
import * as admin from './api/admin.js';
import * as ops from './api/ops.js';
import * as integrity from './api/integrity.js';
import * as extras from './api/extras.js';
import { selfCheck } from './lib/restore.js';
import { notifyOwner } from './lib/notify.js';
import * as profile from './api/profile.js';
import { runBackup } from './lib/backup.js';
import * as settings from './api/settings.js';

function compile(pattern) {
  const keys = [];
  const regex = new RegExp('^' + pattern.replace(/\/:([^/]+)/g, (_, key) => { keys.push(key); return '/([^/]+)'; }) + '$');
  return { regex, keys };
}

const ROUTES = [
  ['GET', '/api/teacher/setup-status', teacher.setupStatus],
  ['POST', '/api/teacher/setup', teacher.setup],
  ['POST', '/api/teacher/login', teacher.login],
  ['POST', '/api/teacher/signup', teacher.signup],
  ['POST', '/api/license/redeem', admin.redeemCode],
  ['POST', '/api/teacher/logout', teacher.logout],
  ['POST', '/api/teacher/change-password', teacher.changePassword],
  ['GET', '/api/teacher/me', teacher.me],

  ['GET', '/api/admin/teachers', admin.listTeachers],
  ['POST', '/api/admin/invites', admin.createInvite],
  ['POST', '/api/admin/codes', admin.createCodes],
  ['GET', '/api/admin/codes', admin.listCodes],
  ['DELETE', '/api/admin/codes/:id', admin.deleteCode],
  ['POST', '/api/admin/teachers/:id/license', admin.setLicense],
  ['GET', '/api/admin/settings', admin.getAdminSettings],
  ['POST', '/api/admin/settings', admin.setAdminSettings],
  ['GET', '/api/admin/audit', admin.listAudit],
  ['POST', '/api/admin/telegram-test', admin.telegramTest],
  ['POST', '/api/admin/backup-now', admin.backupNow],
  ['GET', '/api/admin/backups', admin.backupList],
  ['GET', '/api/admin/backups/:id/download', admin.backupDownload],
  ['POST', '/api/admin/restore/verify', ops.restoreVerify],
  ['POST', '/api/admin/restore/apply', ops.restoreApply],
  ['GET', '/api/readiness', ops.readiness],
  ['GET', '/api/sessions/:sessionId/readiness', ops.sessionReadiness],
  ['GET', '/api/sessions/:sessionId/publish-preview', ops.publishPreview],
  ['POST', '/api/sessions/:sessionId/unpublish', ops.unpublishSession],
  ['DELETE', '/api/admin/invites/:id', admin.revokeInvite],
  ['POST', '/api/admin/teachers/:id/reset-link', admin.createResetLink],
  ['POST', '/api/admin/teachers/:id/active', admin.setTeacherActive],
  ['GET', '/api/invite/:token', admin.inviteInfo],
  ['POST', '/api/invite/:token/accept', admin.acceptInvite],
  ['GET', '/api/teachers/search', admin.searchTeachers],
  ['GET', '/api/export', admin.exportData],
  ['GET', '/api/profile/paper', profile.getPaperProfile],
  ['POST', '/api/profile/paper', profile.setPaperProfile],
  ['GET', '/api/shares', admin.listShares],
  ['POST', '/api/shares', admin.setShare],
  ['POST', '/api/shares/remove', admin.removeShare],

  ['GET', '/api/classes', classes.listClasses],
  ['POST', '/api/classes', classes.createClass],
  ['GET', '/api/classes/:classId/students', classes.listStudents],
  ['POST', '/api/classes/:classId/students', classes.addStudent],
  ['PUT', '/api/students/:studentId', classes.updateStudent],
  ['DELETE', '/api/classes/:classId', classes.deleteClass],
  ['POST', '/api/classes/:classId/settings', classes.classSettings],
  ['DELETE', '/api/students/:studentId', classes.deleteStudent],
  ['DELETE', '/api/classes/:classId/students/:studentId', classes.deleteStudent],
  ['POST', '/api/classes/:classId/students/bulk', classes.importRoster],

  ['GET', '/api/settings/pin', settings.getPinStatus],
  ['POST', '/api/settings/pin', settings.setPin],

  ['GET', '/api/tests', tests.listTests],
  ['POST', '/api/tests', tests.createTest],
  ['GET', '/api/tests/:testId', tests.getTest],
  ['PUT', '/api/tests/:testId', tests.updateTest],
  ['DELETE', '/api/tests/:testId', tests.deleteTest],
  ['POST', '/api/tests/:testId/duplicate', tests.duplicateTest],
  ['POST', '/api/tests/:testId/sample', tests.setSample],
  ['POST', '/api/tests/:testId/rescore', tests.rescoreTest],
  ['POST', '/api/tests/:testId/questions/copy', tests.copyQuestions],
  ['POST', '/api/tests/:testId/questions/bulk', tests.bulkAdd],
  ['GET', '/api/bank', tests.listBank],
  ['POST', '/api/bank/generate', tests.generateTest],
  ['GET', '/api/bank/home', tests.bankHome],
  ['GET', '/api/curriculum', tests.getCurriculum],
  ['POST', '/api/curriculum/lesson', tests.addLesson],
  ['POST', '/api/bank/tag', tests.tagQuestions],
  ['POST', '/api/tests/:testId/questions', tests.addQuestion],
  ['PUT', '/api/questions/:questionId', tests.updateQuestion],
  ['DELETE', '/api/questions/:questionId', tests.deleteQuestion],
  ['POST', '/api/questions/:questionId/notes', tests.addNote],
  ['POST', '/api/notes/:noteId/resolve', tests.resolveNote],
  ['DELETE', '/api/notes/:noteId', tests.deleteNote],

  ['POST', '/api/images', images.upload],
  ['GET', '/api/images/:key', images.serve],

  ['GET', '/api/sessions', sessions.listSessions],
  ['POST', '/api/sessions', sessions.createSession],
  ['GET', '/api/sessions/:sessionId', sessions.getSession],
  ['GET', '/api/sessions/:sessionId/analysis', sessions.sessionAnalysis],
  ['POST', '/api/sessions/:sessionId/pin', sessions.updateSessionPin],
  ['POST', '/api/sessions/:sessionId/close', sessions.closeSession],
  ['POST', '/api/sessions/:sessionId/extend', sessions.extendSession],
  ['POST', '/api/sessions/:sessionId/force-submit', sessions.forceSubmit],
  ['POST', '/api/sessions/:sessionId/reset-device', sessions.resetDevice],
  ['POST', '/api/sessions/:sessionId/rescore', sessions.rescoreOne],
  ['GET', '/api/sessions/:sessionId/writing-marks', sessions.getWritingMarks],
  ['POST', '/api/sessions/:sessionId/writing-marks', sessions.setWritingMarks],
  ['POST', '/api/sessions/:sessionId/writing', sessions.setWritingScore],
  ['POST', '/api/sessions/:sessionId/writing-bulk', sessions.setWritingScoresBulk],
  ['POST', '/api/sessions/:sessionId/reset-student', sessions.resetStudentSession],
  ['DELETE', '/api/sessions/:sessionId', sessions.deleteSession],
  ['POST', '/api/sessions/:sessionId/publish', sessions.publishSession],

  ['GET', '/api/year/class/:classId', year.getYear],
  ['POST', '/api/year/assessment/:id', year.updateAssessment],
  ['POST', '/api/year/assessment/:id/scores', year.saveScores],
  ['POST', '/api/year/config', year.setConfig],

  ['POST', '/api/student/login', student.login],
  ['POST', '/api/student/logout', student.logout],
  ['GET', '/api/student/status', student.status],
  ['GET', '/api/student/review', student.review],
  ['GET', '/api/sessions/:sessionId/review/:studentId', student.teacherReview],
  ['POST', '/api/student/start', student.start],
  ['GET', '/api/student/heartbeat', student.heartbeat],
  ['GET', '/api/student/test', student.getTest],
  ['POST', '/api/student/answer', student.answer],
  ['POST', '/api/student/submit', student.submit],
  ['POST', '/api/student/left-page', student.leftPage],
  ['POST', '/api/student/events', integrity.postEvents],
  ['GET', '/api/student/practice', extras.practice],
  ['POST', '/api/variants/preview', extras.variantPreview],
  ['GET', '/api/student/progress', extras.progress],
  ['GET', '/api/sessions/:sessionId/suspicion', extras.suspicion],
  ['POST', '/api/sessions/:sessionId/writing-grid', extras.writingGrid],
  ['GET', '/api/admin/images/unused', extras.unusedImages],
  ['POST', '/api/admin/images/cleanup', extras.cleanupImages],
  ['POST', '/api/admin/backup-check', extras.backupSelfCheck],
  ['POST', '/api/sessions/:sessionId/integrity', integrity.setIntegrity],
  ['POST', '/api/sessions/:sessionId/lock', integrity.lockStudent],
  ['GET', '/api/sessions/:sessionId/activity', integrity.studentActivity],
  ['POST', '/api/sessions/:sessionId/notes', integrity.addSessionNote],
  ['DELETE', '/api/sessions/:sessionId/notes/:noteId', integrity.deleteSessionNote],
  ['GET', '/api/overview', sessions.overview],
].map(([method, pattern, handler]) => ({ method, handler, ...compile(pattern) }));

export default {
  // Weekly backup (cron in wrangler.toml): Sunday 20:00 UTC = Monday 03:00 in Cambodia.
  async scheduled(event, env, ctx) {
    ctx.waitUntil((async () => {
      await runBackup(env, { reason: 'weekly' });
      // prove the backup we just made can be read; tell the owner if not
      const c = await selfCheck(env);
      await env.DB.prepare("INSERT INTO audit_log (action, detail) VALUES ('backup_check', ?1)").bind(JSON.stringify(c).slice(0, 400)).run();
      if (!c.ok) await notifyOwner(env, `⚠️ ការបម្រុងទុកប្រចាំសប្តាហ៍មានបញ្ហា៖ ${c.problem}`);
    })());
  },

  async fetch(req, env, ctx) {
    const url = new URL(req.url);

    if (url.pathname.startsWith('/api/')) {
      for (const route of ROUTES) {
        if (route.method !== req.method) continue;
        const match = route.regex.exec(url.pathname);
        if (!match) continue;
        const params = Object.fromEntries(route.keys.map((key, i) => [key, match[i + 1]]));
        try {
          return await route.handler(req, env, params, ctx);
        } catch (e) {
          return err(e.message || 'Something went wrong.', 500);
        }
      }
      return err('Not found.', 404);
    }

    return env.ASSETS.fetch(req);
  },
};
