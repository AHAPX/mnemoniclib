from sqlalchemy.orm.exc import NoResultFound


class MnemonicExceptionBase(Exception):
    pass


class WordNotFound(MnemonicExceptionBase):
    pass


class CharNotFound(MnemonicExceptionBase):
    pass
