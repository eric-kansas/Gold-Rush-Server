
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime
from sqlalchemy.orm import relation, synonym

from tg2app.model import DeclarativeBase, metadata, DBSession
from tg2app.model.player import Player
from tg2app.model.gameObject import GameObject

class Hand(DeclarativeBase):
    __tablename__ = 'tg_hand'

    #( Columns

    hand_id = Column(Integer, autoincrement=True, primary_key=True)

    # TODO -- cards

    game_id = Column(Integer, ForeignKey(GameObject.id))
    player_id = Column(Integer, ForeignKey(Player.id))
