import json

import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.session import async_session
from bot.database.dals import ComponentDAL, ButtonDAL
from bot.config import CONSTRUCTOR_API_HOST


async def migrate_test(session: AsyncSession, data: list):
    await ButtonDAL.delete(session)
    await ComponentDAL.delete(session)
    data.reverse()
    for component in data:
        await ComponentDAL.create(
            session, id=component['id'], content=component['content'], type=component['type'],
            next_component_id=component['next_component_id']
        )

        for button in component['buttons']:
            await ButtonDAL.create(
                session, id=button['id'], text=button['content'], component_id=component['id'],
                next_component_id=button['next_component_id']
            )


async def request_test_from_api(test_id: int):
    async with aiohttp.ClientSession() as http_session:
        async with http_session.get(f'{CONSTRUCTOR_API_HOST}/api/test/{test_id}/import') as response:
            return await response.json()


async def import_test(db_session: AsyncSession, test_id: int):
    data = await request_test_from_api(test_id)
    await migrate_test(db_session, data)


if __name__ == '__main__':
    import asyncio


    async def main():
        async with async_session() as session:
            with open('test.json') as file:
                data = file.read()
                json_data: list = json.loads(data)
            json_data.reverse()

            await migrate_test(session, json_data)


    asyncio.run(main())
