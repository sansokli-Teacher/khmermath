-- #489: 12.9+12.89+13.21+13.4 = 52.4 (the option read 52.37)
UPDATE test_questions SET options_json = '["\\(28.431\\)", "\\(52.4\\)", "\\(40.86\\)", "\\(29.286\\)"]' WHERE id = 489 AND test_id = 10;
-- the book writes កម្រៃជើងសា (not ជើងសារ)
UPDATE test_questions SET stem_text = REPLACE(stem_text, 'ជើងសារ', 'ជើងសា'), solution_text = REPLACE(solution_text, 'ជើងសារ', 'ជើងសា') WHERE test_id = 10 AND grade = '7' AND (stem_text LIKE '%ជើងសារ%' OR solution_text LIKE '%ជើងសារ%');
