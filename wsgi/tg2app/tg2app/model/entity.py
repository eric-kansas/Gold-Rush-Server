from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, Boolean
from sqlalchemy.orm import relation, synonym

from tg2app.model import DeclarativeBase, metadata, DBSession

from tg2app.model.game import Game
from tg2app.model.game import Player

class Entity(DeclarativeBase):
    __tablename__ = 'entity'

    id = Column(Integer, autoincrement=True, primary_key=True)

    #if flase is a stake
    is_avatar = Column(Boolean)

    #grid pos
    row = Column(Integer)
    col = Column(Integer)

    #index of player in client game array
    in_game_id = Column(Integer) 

    #relations
    game_id = Column(Integer, ForeignKey(Game.id))
    player_id = Column(Integer, ForeignKey(Player.id))

    def to_json(self, no_relations=False):
        if no_relations:
            return {
                'id': self.id,
                'is_avatar': self.is_avatar,
		        'row': self.row,
		        'col': self.col,
                'in_game_id': self.in_game_id,
		        'type': self.__tablename__,
            }
        else:
            return {
                'id': self.id,
                'is_avatar': self.is_avatar,
		        'row': self.row,
		        'col': self.col,
                'in_game_id': self.in_game_id,
		        'type': self.__tablename__,
		        'game': self.game.to_json(no_relations=True),
            }
