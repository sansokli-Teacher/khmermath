// What a visitor can try for free, and what the paid plans cost. Payments are handled by the owner
// (bank transfer / Telegram): the teacher asks for an unlock code, pays, and the owner issues a code
// for 1 or 12 months from the "Teachers" tab. Prices are shown in the app, so change them here only.
export const TRIAL = { classes: 1, students: 10, tests: 2, questions: 10, sessions: 2 };

export const PLANS = {
  month: { id: 'month', months: 1, price: 2.99, label: '១ ខែ' },
  year: { id: 'year', months: 12, price: 15, was: 30, label: '១ ឆ្នាំ', note: 'បញ្ចុះតម្លៃពិសេស' },
};
