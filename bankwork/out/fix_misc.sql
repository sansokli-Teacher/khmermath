-- #489: 12.9+12.89+13.21+13.4 = 52.4 (the option read 52.37)
UPDATE test_questions SET options_json = '["\\(28.431\\)", "\\(52.4\\)", "\\(40.86\\)", "\\(29.286\\)"]' WHERE id = 489 AND test_id = 10;
-- the book writes កម្រៃជើងសា (not ជើងសារ)
UPDATE test_questions SET stem_text = REPLACE(stem_text, 'ជើងសារ', 'ជើងសា'), solution_text = REPLACE(solution_text, 'ជើងសារ', 'ជើងសា') WHERE test_id = 10 AND grade = '7' AND (stem_text LIKE '%ជើងសារ%' OR solution_text LIKE '%ជើងសារ%');
-- L7 notation of the new book: litre is ℓ, day is d, and the farm unit is ហិកតា
UPDATE test_questions SET
 stem_text = REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(stem_text,'\text{dl}','\text{d}\ell'),'\text{cl}','\text{c}\ell'),'\text{hl}','\text{h}\ell'),'\text{l}','\ell'),'\text{j}','\text{d}'),
 solution_text = REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(solution_text,'\text{dl}','\text{d}\ell'),'\text{cl}','\text{c}\ell'),'\text{hl}','\text{h}\ell'),'\text{l}','\ell'),'\text{j}','\text{d}'),
 options_json = REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(options_json,'\\text{dl}','\\text{d}\\ell'),'\\text{cl}','\\text{c}\\ell'),'\\text{hl}','\\text{h}\\ell'),'\\text{l}','\\ell'),'\\text{j}','\\text{d}')
WHERE test_id = 10 AND grade = '7' AND (stem_text LIKE '%\text{l}%' OR stem_text LIKE '%\text{dl}%' OR stem_text LIKE '%\text{cl}%' OR stem_text LIKE '%\text{hl}%' OR stem_text LIKE '%\text{j}%' OR solution_text LIKE '%\text{l}%' OR solution_text LIKE '%\text{dl}%' OR solution_text LIKE '%\text{cl}%' OR solution_text LIKE '%\text{hl}%' OR solution_text LIKE '%\text{j}%' OR options_json LIKE '%\\text{l}%' OR options_json LIKE '%\\text{dl}%' OR options_json LIKE '%\\text{cl}%' OR options_json LIKE '%\\text{hl}%' OR options_json LIKE '%\\text{j}%');
UPDATE test_questions SET stem_text = REPLACE(REPLACE(stem_text,'ហិចតូ','ហិកតូ'),'ហិចតា','ហិកតា'), solution_text = REPLACE(REPLACE(solution_text,'ហិចតូ','ហិកតូ'),'ហិចតា','ហិកតា'), options_json = REPLACE(REPLACE(options_json,'ហិចតូ','ហិកតូ'),'ហិចតា','ហិកតា') WHERE test_id = 10 AND grade = '7' AND (stem_text LIKE '%ហិចត%' OR solution_text LIKE '%ហិចត%' OR options_json LIKE '%ហិចត%');
-- angle units in the new book: មីនុត and សេកុង (not ទីនុត / ស៊ីគុង)
UPDATE test_questions SET stem_text = REPLACE(REPLACE(stem_text,'ទីនុត','មីនុត'),'ស៊ីគុង','សេកុង'), solution_text = REPLACE(REPLACE(solution_text,'ទីនុត','មីនុត'),'ស៊ីគុង','សេកុង'), options_json = REPLACE(REPLACE(options_json,'ទីនុត','មីនុត'),'ស៊ីគុង','សេកុង') WHERE test_id = 10 AND grade = '7' AND (stem_text LIKE '%ទីនុត%' OR stem_text LIKE '%ស៊ីគុង%' OR solution_text LIKE '%ទីនុត%' OR solution_text LIKE '%ស៊ីគុង%' OR options_json LIKE '%ទីនុត%' OR options_json LIKE '%ស៊ីគុង%');
-- the book spells Jamaica ចាម៉ីកា
UPDATE test_questions SET stem_text = REPLACE(stem_text,'ហ្សាម៉ាអ៊ិក','ចាម៉ីកា'), solution_text = REPLACE(solution_text,'ហ្សាម៉ាអ៊ិក','ចាម៉ីកា') WHERE test_id = 10 AND grade = '7' AND (stem_text LIKE '%ហ្សាម៉ាអ៊ិក%' OR solution_text LIKE '%ហ្សាម៉ាអ៊ិក%');
