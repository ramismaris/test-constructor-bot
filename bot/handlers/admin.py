from aiogram import Router, types

from bot.filters.role import RoleFilter

router = Router()


@router.message(RoleFilter('admin'))
async def foo(message: types.Message):
    await message.answer('Good day, sir.')
