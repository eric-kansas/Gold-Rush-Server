
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime
from sqlalchemy.orm import relation, synonym

from tg2app.model import DeclarativeBase, metadata, DBSession

class Hand(DeclarativeBase):
    __tablename__ = 'tg_hand'

    #( Columns

    hand_id = Column(Integer, autoincrement=True, primary_key=True)
