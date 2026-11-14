# -*- coding: utf-8 -*-
"""KhmerMath Question Bank: Grade 12 Social science (SS), Chapter 2: ដេរីវេនៃអនុគមន៍, lesson 2: អនុវត្តន៍នៃដេរីវេ.
The SS book (Math G12 (SS).book, chapter 2 lesson 2) has the same text, examples and exercises as the Grade 12 Science
lesson C3-L2.tex (Lesson/G12/SC), so this question set is the Science set G12L07 re-tagged for grade 12SS and its SS chapter.
Every answer, figure and Bloom level is the one already computed and numerically verified in G12L07."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.dirname(__file__))
import G12L07 as B

LESSON = B.LESSON
CHAPTER = 'ជំពូកទី 2 : ដេរីវេនៃអនុគមន៍'
GRADE = '12SS'
TARGET = B.TARGET
TOPIC_MAP = B.TOPIC_MAP
ORDER_BASE = 30400


def cands():
    return B.cands()


def verify():
    return B.verify()

