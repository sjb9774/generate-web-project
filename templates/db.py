from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from {$name}.config import config

def new_engine(uri=None):
    if not uri:
        uri = config.database.uri
    return create_engine(uri)
engine = new_engine()
my_session_maker = scoped_session(sessionmaker(bind=engine))

Session = my_session_maker()
Base = declarative_base()

def initialize():
    global Session
    global Base
    global my_session_maker
    global engine
    engine.dispose()
    engine = new_engine()
    my_session_maker = scoped_session(sessionmaker(bind=engine))
    Session = my_session_maker()
    Base.metadata.bind = engine
    Base.metadata.create_all()

class IdMixin():

    def __init__(self, **kwargs):
        for attr, val in kwargs.iteritems():
            if hasattr(self, attr):
                setattr(self, attr, val)
        from uuid import uuid4
        self.id = str(uuid4())

    @declared_attr
    def id(cls):
        return Column(VARCHAR(40), name='id', primary_key=True)


class DefaultMixin():

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()+'s'

    def insert(self, commit=True):
        Session.add(self)
        if commit:
            Session.commit()
        return self

    def delete(self, commit=True):
        Session.delete(self)
        if commit:
            Session.commit()
        return self

    def update(self, **kwargs):
        commit = kwargs.pop('commit', False)
        for attr, val in kwargs.iteritems():
            if hasattr(self, attr):
                setattr(self, attr, val)
        if commit:
            Session.commit()
        return self

    @classmethod
    def get(self, id):
        return Session.query(self).get(id)

    @classmethod
    def all(self):
        return Session.query(self).filter(self.id != None)

    @classmethod
    def filter(self, *args, **kwargs):
        return Session.query(self).filter(*args, **kwargs)

    @classmethod
    def filter_by(self, **kwargs):
        return Session.query(self).filter_by(**kwargs)
