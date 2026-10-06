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
  ['DELETE', '/api/admin/invites/:id', admin.revokeInvite],
  ['POST', '/api/admin/teachers/:id/reset-link', admin.createResetLink],
  ['POST', '/api/admin/teachers/:id/active', admin.setTeacherActive],
  ['GET', '/api/invite/:token', admin.inviteInfo],
  ['POST', '/api/invite/:token/accept', admin.acceptInvite],
  ['GET', '/api/teachers/search', admin.searchTeachers],
  ['GET', '/api/shares', admin.listShares],
  ['POST', '/api/shares', admin.setShare],
  ['POST', '/api/shares/remove', admin.removeShare],

  ['GET', '/api/classes', classes.listClasses],
  ['POST', '/api/classes', classes.createClass],
  ['GET', '/api/classes/:classId/students', classes.listStudents],
  ['POST', '/api/classes/:classId/students', classes.addStudent],
  ['PUT', '/api/students/:studentId', classes.updateStudent],
  ['DELETE', '/api/classes/:classId', classes.deleteClass],
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
  ['GET', '/api/student/test', student.getTest],
  ['POST', '/api/student/answer', student.answer],
  ['POST', '/api/student/submit', student.submit],
  ['POST', '/api/student/left-page', student.leftPage],
  ['GET', '/api/overview', sessions.overview],
].map(([method, pattern, handler]) => ({ method, handler, ...compile(pattern) }));

export default {
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
