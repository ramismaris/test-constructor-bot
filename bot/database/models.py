from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)

    tg_id = Column(String, unique=True)
    role = Column(String)
    test_is_finished = Column(Boolean, nullable=True)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __str__(self):
        return f'{self.id} - {self.tg_id}'


class Node(Base):
    __tablename__ = 'nodes'

    id = Column(Integer, primary_key=True)


class NodeBlock(Base):
    __tablename__ = 'node_blocks'

    id = Column(Integer, primary_key=True)

    content = Column(String, nullable=True)
    block_type = Column(String)
    block_types = [
        'text',
        'input',
        'button',
    ]
    node_id = Column(ForeignKey('nodes.id'))
    next_node_id = Column(ForeignKey(f'{Node.__tablename__}.id'), nullable=True)


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True)
    answer = Column(String)
    node_block_id = Column(ForeignKey('node_blocks.id'))
    user_id = Column(Integer, ForeignKey("users.id"))

    def __str__(self):
        return f'{self.id} - {self.question} - {self.user_id}'


class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True)
    is_checked = Column(Boolean)
    user_id = Column(Integer, ForeignKey("users.id"))
    manager_id = Column(Integer, ForeignKey("users.id"))


class AnswersMark(Base):
    __tablename__ = "answers_mark"

    id = Column(Integer, primary_key=True)
    answer_id = Column(Integer, ForeignKey("answers.id"))
    score = Column(Integer)
    manager_id = Column(Integer, ForeignKey("users.id"))
