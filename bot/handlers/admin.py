from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.role import RoleFilter
from bot.utils.import_test import import_test


class TestQuery(StatesGroup):
    number = State()


router = Router()


@router.message(RoleFilter('admin'), CommandStart())
async def admin_menu(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(text='📥Импортировать тест', callback_data=f'admin_import_test')
    ]])
    await message.answer('<b>📚Меню администратора</b>', parse_mode='HTML', reply_markup=keyboard)


@router.callback_query(F.data == 'admin_import_test')
async def admin_import_test_query(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.answer('Введите ID теста, чтобы импортировать его')

    await state.set_state(TestQuery.number)


@router.message(TestQuery.number)
async def admin_take_test_id(message: types.Message, session: AsyncSession, state: FSMContext):
    test_id = message.text

    if not test_id.isdigit():
        await message.answer('ID теста является числом')
        return

    test_id = int(test_id)
    await import_test(session, test_id)

    await message.answer('Успешно импортировано✅')

    await state.set_state(None)
