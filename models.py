from sqlalchemy import create_engine, Integer, String, Column, Date, ForeignKey, Boolean

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, Column, Date, ForeignKey
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker, scoped_session

# engine = create_engine('mysql+pymysql://root:root@localhost:3306/mydb')
engine = create_engine('mysql+pymysql://root:OlehSyniuk@localhost:3306/pp')

SessionFactory = sessionmaker(bind=engine)

Session = scoped_session(SessionFactory)

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(45))
    surname = Column(String(45))
    username = Column(String(45))
    password = Column(String(45))


class Audience(Base):
    __tablename__ = 'audience'
    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    amount_of_places = Column(Integer)
    status = Column(Boolean)


class Reservation(Base):
    __tablename__ = 'reservation'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    title = Column(String(45))
    audience_id = Column(Integer, ForeignKey('audience.id'))
    from_date = Column(DATETIME)
    to_date = Column(DATETIME)
    audience = relationship("Audience")
    user = relationship("User")