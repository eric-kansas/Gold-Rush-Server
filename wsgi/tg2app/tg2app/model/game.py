
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

    # Don't use this.  Just use 'whose_turn'.  It needs to be here, though.
    whose_turn_id = Column(Integer, ForeignKey(Player.id))

    # A list of games in which I have the next turn
    hands = relation("Hand", backref="game")

Game.__mapper__.add_property('players', relation(
    Player,
    primaryjoin=Player.id==players_to_game_mapping.c.player_id,
    secondaryjoin=players_to_game_mapping.c.game_id==Game.id,
    secondary=players_to_game_mapping,
    backref=backref('games')
))
