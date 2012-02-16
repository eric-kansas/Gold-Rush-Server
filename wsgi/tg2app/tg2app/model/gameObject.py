
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, Boolean
from sqlalchemy.orm import relation, synonym

from tg2app.model import DeclarativeBase, metadata, DBSession

class GameObject(DeclarativeBase):
    __tablename__ = 'tg_gameObject'

    id = Column(Integer, primary_key=True)
    #( Columns

    is_avatar = Column(Boolean)
    is_stake = Column(Boolean)
    row = Column(Integer)
    col = Column(Integer) 
