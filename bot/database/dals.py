from sqlalchemy import select, update, desc, asc, delete
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import User, Button, Answer, Component


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


class ComponentDAL:
    @staticmethod
    async def create(db_session: AsyncSession, **kwargs) -> Component:
        new_component = Component(**kwargs)
        db_session.add(new_component)
        await db_session.commit()

        return new_component

    @staticmethod
    async def read(db_session: AsyncSession, **kwargs) -> list[Component]:
        stmt = select(Component).filter_by(**kwargs).order_by(asc(Component.id))
        components = await db_session.scalars(stmt)

        return components.fetchall()

    @staticmethod
    async def delete(db_session: AsyncSession, **kwargs):
        stmt = delete(Component).filter_by(**kwargs)
        await db_session.execute(stmt)
        await db_session.commit()
        return True


class ButtonDAL:
    @staticmethod
    async def create(db_session: AsyncSession, **kwargs) -> Button:
        new_button = Button(**kwargs)
        db_session.add(new_button)
        await db_session.commit()

        return new_button

    @staticmethod
    async def read(db_session: AsyncSession, **kwargs) -> list[Button]:
        stmt = select(Button).filter_by(**kwargs)
        Component_blocks = await db_session.scalars(stmt)

        return Component_blocks.fetchall()

    @staticmethod
    async def update(db_session: AsyncSession, block_id: int, **kwargs):
        pass

    @staticmethod
    async def delete(db_session: AsyncSession, **kwargs):
        stmt = delete(Button).filter_by(**kwargs)
        await db_session.execute(stmt)
        await db_session.commit()
        return True


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
