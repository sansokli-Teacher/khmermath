# -*- coding: utf-8 -*-
"""KhmerMath Question Bank: Grade 12 Social science (SS), Chapter 1: លីមីត, lesson 2: ភាពជាប់នៃអនុគមន៍.
The SS book (Math G12 (SS).book, chapter 1 lesson 2) has the same text, examples and exercises as the Grade 12 Science
lesson C2-L2.tex (Lesson/G12/SC), so this question set is the Science set G12L05 re-tagged for grade 12SS and its SS chapter.
Every answer, figure and Bloom level is the one already computed and numerically verified in G12L05."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.dirname(__file__))
import G12L05 as B

LESSON = B.LESSON
CHAPTER = 'ជំពូកទី 1 : លីមីត'
GRADE = '12SS'
TARGET = B.TARGET
TOPIC_MAP = B.TOPIC_MAP
ORDER_BASE = 30200


def cands():
    return B.cands()


def verify():
    return B.verify()
