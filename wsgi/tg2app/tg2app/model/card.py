from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime
from sqlalchemy.orm import relation, synonym

from tg2app.model import DeclarativeBase, metadata, DBSession

class Card(DeclarativeBase):
    __tablename__ = 'tg_card'

    #{ Columns

    card_id = Column(Integer, autoincrement=True, primary_key=True)

    is_up = Column(Boolean)

    #known_by_players = Column()

    suit = Column(Integer)

    kind = Column(Integer)

    #hand = Column()
