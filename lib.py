import random

from sqlalchemy import func 

from database import session, Language, Word, Char
from exc import WordNotFound, NoResultFound, CharNotFound


def get_words(length=0):
    query = session.query(Word)
    if length > 0:
        query = query.filter(Word.length == length)
    return query


def random_word(length=0):
    words = get_words(length)
    count = words.count()
    if count:
        rand_inx = random.randint(0, count-1)
        return str(words[rand_inx])
    raise WordNotFound


def random_char(char):
    try:
        char_obj = session.query(Char).filter(Char.char == char).one()
    except NoResultFound:
        raise CharNotFound
    else:
        return random.choice(char_obj.pairs)


def random_password(length):
    word = ''
    for char in random_word(length):
        word += random_char(char)
    return word


if __name__ == '__main__':
    print random_password(8)
