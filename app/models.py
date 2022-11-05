from sqlalchemy import Integer, String, Column, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(30), unique=True, nullable=False, index=True, comment='Имя пользователя')
    hashed_password = Column(String, comment='Пароль')

    tags = relationship('Tag', back_populates='user')


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=True, comment='Имя тега')
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship('User', back_populates='tags')