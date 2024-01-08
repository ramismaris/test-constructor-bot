from sqlalchemy import select, update, desc
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import User, NodeBlock, Answer, Node


class UserDAL:
    @staticmethod
    async def create(
            db_session: AsyncSession, tg_id: str, role: str = None
    ) -> User:
        new_user = User(
            tg_id=tg_id, role=role,
        )
        db_session.add(new_user)
        await db_session.commit()

        return new_user

    @staticmethod
    async def read(db_session: AsyncSession, **kwargs) -> list[User] | None:
        stmt = select(User).filter_by(**kwargs)
        users = await db_session.scalars(stmt)

        return users.fetchall()

    @staticmethod
    async def update(
            db_session: AsyncSession, user_id: int | None = None, tg_id: str | None = None, **kwargs
    ) -> User | None:
        if user_id:
            result = await db_session.execute(
                update(User).where(User.id == user_id).values(kwargs).returning(User)
            )
            await db_session.commit()
            return result.scalar_one_or_none()
        result = await db_session.execute(
            update(User).where(User.tg_id == tg_id).values(kwargs).returning(User)
        )
        await db_session.commit()
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user(db_session: AsyncSession, user_id: int | None = None, tg_id: str | None = None) -> User | None:
        if user_id:
            user = await db_session.get(User, user_id)
            return user
        result = await db_session.execute(
            select(User).where(User.tg_id == tg_id)
        )
        user = result.scalar_one_or_none()
        return user

    @staticmethod
    async def get_managers(db_session: AsyncSession) -> list[User]:
        stmt = select(User).where(User.role == 'manager')
        users = await db_session.scalars(stmt)

        return users.fetchall()


class NodeDAL:
    @staticmethod
    async def read(db_session: AsyncSession, **kwargs) -> list[Node]:
        stmt = select(Node).filter_by(**kwargs)
        nodes = await db_session.scalars(stmt)

        return nodes.fetchall()


class NodeBlockDAL:
    @staticmethod
    async def create(db_session: AsyncSession, **kwargs) -> NodeBlock:
        pass

    @staticmethod
    async def read(db_session: AsyncSession, **kwargs) -> list[NodeBlock]:
        stmt = select(NodeBlock).filter_by(**kwargs)
        node_blocks = await db_session.scalars(stmt)

        return node_blocks.fetchall()

    @staticmethod
    async def update(db_session: AsyncSession, block_id: int, **kwargs):
        pass


class AnswerDAL:
    @staticmethod
    async def create(db_session: AsyncSession, **kwargs) -> Answer:
        new_answer = Answer(**kwargs)
        db_session.add(new_answer)
        await db_session.commit()

        return new_answer

    @staticmethod
    async def read(db_session: AsyncSession, **kwargs) -> list[Answer]:
        stmt = select(Answer).filter_by(**kwargs)
        answers = await db_session.scalars(stmt)

        return answers.fetchall()
