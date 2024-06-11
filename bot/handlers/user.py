from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.dals import UserDAL, AnswerDAL, ComponentDAL, ButtonDAL

router = Router()


@router.message()
async def on_message(message: types.Message, state: FSMContext, session: AsyncSession):
    user = await UserDAL.get_user(session, tg_id=str(message.chat.id))

    if not user:
        user = await UserDAL.create(session, tg_id=str(message.chat.id), role='user')
        components = await ComponentDAL.read(session)
        await state.update_data(user_id=user.id, last_component_id=None, component_id=components[0].id)

    if user.test_is_finished:
        await message.answer('Вы уже прошли тест :)')
        return

    data = await state.get_data()
    if data is None:
        await message.answer('error 25')
        return

    component_id = data['component_id']
    component = (await ComponentDAL.read(session, id=component_id))[0]
    buttons = await ButtonDAL.read(session, component_id=component_id)

    if not component.next_component_id and len(buttons) == 0:
        await UserDAL.update(session, user_id=user.id, test_is_finished=True)

    await state.update_data(last_component_id=component_id, component_id=component.next_component_id)
    if component.type == 'text':
        keyboard = None
        if len(buttons) > 0:
            button_node_blocks = []
            for button in buttons:
                button_node_blocks.append(button)

            kb_builder = InlineKeyboardBuilder()
            for button in button_node_blocks:
                kb_builder.button(text=button.text, callback_data=f'button_id:{button.id}')

            keyboard = kb_builder.as_markup()

        await message.answer(text=component.content, reply_markup=keyboard)
        next_component_is_text = await ComponentDAL.read(
            session, id=component.next_component_id, type='text'
        )
        if len(next_component_is_text) > 0:
            await on_message(message, state, session)
    elif component.type == 'input':
        last_component = await ComponentDAL.read(session, id=data['last_component_id'], type='text')
        last_component_id = last_component[0].id
        await AnswerDAL.create(session, answer=message.text, component_id=last_component_id, user_id=user.id)
        await on_message(message, state, session)


@router.callback_query(F.data.startswith('button_id'))
async def callback_handler(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback.message.edit_reply_markup(reply_markup=None)

    data = await state.get_data()
    button_id = int(callback.data.split(':')[1])
    button = (await ButtonDAL.read(session, id=button_id))[0]
    user = await UserDAL.get_user(session, tg_id=str(callback.message.chat.id))

    await state.update_data(last_component_id=data['component_id'], component_id=button.next_component_id)

    await AnswerDAL.create(session, answer=button.text, component_id=button.component_id, user_id=user.id)

    await on_message(callback.message, state, session)
