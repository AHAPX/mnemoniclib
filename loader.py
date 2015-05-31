#!/usr/bin/env python
import os
import argparse

from database import session, Language, Word, Char
from exc import NoResultFound

STOP_CHARS = '!@#$%^&*()_+-=\\/,.{}[]:;\'"0123456789'


def has_stop_char(word):
    for char in STOP_CHARS:
        if char in word:
            return True
    return False


parser = argparse.ArgumentParser()
parser.add_argument('-l', '--lang', default='en', type=str, help='word file')
parser.add_argument('file', type=str, help='word file')
parser.add_argument('-c', '--chars', action="store_true", help='chars file')
args = parser.parse_args()

try:
    lang = session.query(Language).filter(Language.name == args.lang.lower()).one()
except NoResultFound:
    lang = Language(name=args.lang.lower())
    session.add(lang)
    session.commit()

if args.chars:
    added, changed = 0, 0
    f = open(args.file)
    for line in f:    
        line = line.strip()
        if line:
            char = line[0]
            try:
                char_obj = session.query(Char).filter(Char.char == char).one()
                changed += 1
            except NoResultFound:
                char_obj = Char(char=char)
                session.add(char_obj)
                added += 1
            char_obj.pairs = char + char.upper() + line[1:]
            session.commit()
    print '{} char added, {} chars changed'.format(added, changed)
else:
    added, existed = 0, 0
    f = open(args.file)
    for line in f:
        line = line.strip()
        if line and not has_stop_char(line):
            word = line.lower()
            try:
                session.query(Word).filter(Word.word == word).one()
                existed += 1
            except NoResultFound:
                session.add(Word(word=word, length=len(word), language=lang))
                session.commit()
                added += 1
    print '{} words added, {} existed already'.format(added, existed)
