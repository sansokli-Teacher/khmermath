-- Adds the Bloom level to the central question bank. Nullable: existing rows stay NULL, existing INSERTs keep working.
ALTER TABLE test_questions ADD COLUMN bloom TEXT;
