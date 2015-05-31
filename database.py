from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Language(Base):
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return 'Lang({})'.format(self.name)

    def __str__(self):
        return self.name


class Word(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    word = Column(String)
    length = Column(Integer)
    language_id = Column(Integer, ForeignKey('languages.id'))
    language = relationship('Language', backref=backref('languages', order_by=id))

    def __repr__(self):
        return 'Word({}, length={}, language={})'.format(self.word, self.length, self.language.name)

    def __str__(self):
        return self.word


class Char(Base):
    __tablename__ = 'chars'

    id = Column(Integer, primary_key=True)
    char = Column(String)
    pairs = Column(String)

    def __rept__(self):
        return 'Char({}, {})'.format(self.char, self.pairs)

    def __str__(self):
        return self.char


engine = create_engine('sqlite:///mnemonic.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
