UPDATE test_questions SET
  stem_text = REPLACE(REPLACE(stem_text, 'PGCD', 'GCD'), 'PPCM', 'LCM'),
  options_json = REPLACE(REPLACE(options_json, 'PGCD', 'GCD'), 'PPCM', 'LCM'),
  solution_text = REPLACE(REPLACE(solution_text, 'PGCD', 'GCD'), 'PPCM', 'LCM')
WHERE test_id = 10 AND grade = '7' AND (stem_text LIKE '%PGCD%' OR stem_text LIKE '%PPCM%' OR options_json LIKE '%PGCD%' OR options_json LIKE '%PPCM%' OR solution_text LIKE '%PGCD%' OR solution_text LIKE '%PPCM%');
