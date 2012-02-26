from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, Boolean
from sqlalchemy.orm import relation, synonym

from tg2app.model import DeclarativeBase, metadata, DBSession
from tg2app.model.hand import Hand
from tg2app.model.game import Game

class Card(DeclarativeBase):
    __tablename__ = 'tg_card'

    #{ Columns
    card_id = Column(Integer, autoincrement=True, primary_key=True)

    #is this card visible
    is_up = Column(Boolean)

    #kind and suit of card
    suit = Column(Unicode(255))
    kind = Column(Integer)

    #grid pos in game
    row = Column(Integer)
    col = Column(Integer)

    #is this card minable
    minable = Column(Boolean)

    #what index am I in in the clients game
    in_game_id = Column(Integer)

    #relations
    game_id = Column(Integer, ForeignKey(Game.id))

    def to_json(self, no_relations=False):
        if no_relations:
            return {
                'id': self.card_id,
                'is_up': self.is_up,
		        'suit': self.suit,
		        'kind': self.kind,
                'row': self.row,
                'col': self.col,
                'minable': self.minable,
                'in_game_id': self.in_game_id,
		        'type': self.__tablename__,
            }
        else:
            return {
                'id': self.card_id,
                'is_up': self.is_up,
		        'suit': self.suit,
		        'kind': self.kind,
        		'type': self.__tablename__,
                'row': self.row,
                'col': self.col,
                'minable': self.minable,
                'in_game_id': self.in_game_id,
                'game_id': self.game_id,
            }
