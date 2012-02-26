
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, Boolean
from sqlalchemy.orm import relation, synonym, backref

from tg2app.model import DeclarativeBase, metadata, DBSession

from tg2app.model.player import Player

players_to_game_mapping = Table(
    'players_to_game_mapping', metadata,
    Column('player_id', Integer,
           ForeignKey('player.id'), primary_key=True),
    Column('game_id', Integer,
           ForeignKey('game.id'), primary_key=True))

class Game(DeclarativeBase):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True)
    
    game_state = Column(Integer)

    game_turn =  Column(Integer)

    #current player in client game
    current_player = Column(Integer)

    #last roll
    current_roll = Column(Integer)

    #pointer to what facebook players turn it is
    whose_turn_id = Column(Integer, ForeignKey(Player.id))

    # a list of entities (avatars and stakes) in the current game
    entities = relation("Entity", backref="game")

    # a list of cards (the board) in the current game
    cards = relation("Card", backref="game")
    players = relation(
        "Player",
        secondary=players_to_game_mapping,
        backref="games",
    )

    def to_json(self, no_relations=False):
        if no_relations:
            return {
                'id': self.id,
				'type': self.__tablename__,
                'current_player': self.current_player,
                'current_roll': self.current_roll,
                'game_state': self.game_state,
                'game_turn': self.game_turn,
            }
        else:
            return {
                'id': self.id,
				'type': self.__tablename__,
                'current_player': self.current_player,
                'current_roll': self.current_roll,
                'game_state': self.game_state,
                'game_turn': self.game_turn,
                'whose_turn': self.whose_turn.to_json(),
                'entities': [ent.to_json() for ent in self.entities],
                'cards': [card.to_json() for card in self.cards],
                'players': [player.to_json() for player in self.players],
            }
