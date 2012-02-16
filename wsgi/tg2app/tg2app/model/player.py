# -*- coding: utf-8 -*-
"""Player model."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.orm import relation, backref

from tg2app.model import DeclarativeBase, metadata, DBSession

friends_mapping = Table(
    'friends_mapping', metadata,
    Column('left_id', Integer,
           ForeignKey('player.id'), primary_key=True),
    Column('right_id', Integer,
           ForeignKey('player.id'), primary_key=True))

class Player(DeclarativeBase):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), nullable=False)

Player.__mapper__.add_property('friends', relation(
    Player,
    primaryjoin=Player.id==friends_mapping.c.left_id,
    secondaryjoin=friends_mapping.c.right_id==Player.id,
    secondary=friends_mapping,
    backref=backref('friends_backref')
))

