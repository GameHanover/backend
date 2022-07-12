""" Database Module """
from datetime import date

from dateutil.relativedelta import relativedelta
from sqlalchemy import (Column, Integer, String, Boolean, Date, ForeignKey,
                        Enum)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import expression
from app import DB


class Address(DB.Model):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True, autoincrement=True)
    address1 = Column(String(100))
    address2 = Column(String(100))
    city = Column(String(50))
    state = Column(String(50))
    zip_code = Column(String(15))
    coaches = relationship("Coach",
                            back_populates="address")

class Person(DB.Model):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    address_id = Column(Integer, ForeignKey('address.id'))
    phone_nbr = Column(String)
    table_type = Column(String(20))
    address = relationship("Address",
                          back_populates="coaches")
    __mapper_args__ = {
        'polymorphic_identity': 'person',
    }


class Coach(Person):
    __tablename__ = 'coach'
    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    active = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity':'coach',
    }


class Field(DB.Model):
    __tablename__ = 'field'
    id = Column(Integer, primary_key=True, autoincrement=True)
    address_id = Column(Integer, ForeignKey('address.id'))
    active = Column(Boolean)


class Game(DB.Model):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True, autoincrement=True) 
    game_dt = Column(Date)
    field_id = Column(Integer, ForeignKey('field.id'))
    coach_id = Column(Integer, ForeignKey('coach.id'))
