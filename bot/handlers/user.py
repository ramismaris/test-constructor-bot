from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.dals import UserDAL, AnswerDAL, NodeDAL, NodeBlockDAL

router = Router()


@router.message()
async def on_message(message: types.Message, state: FSMContext, session: AsyncSession):
    user = await UserDAL.get_user(session, tg_id=str(message.chat.id))
    if not user:
        user = await UserDAL.create(session, tg_id=str(message.chat.id), role='user')
        nodes = await NodeDAL.read(session)
        await state.update_data(user_id=user.id, last_node_id=None, node_id=nodes[0].id)

    if user.test_is_finished:
        await message.answer('Вы уже прошли тест :)')
        return

    data = await state.get_data()
    if data is None:
        await message.answer('error 25')
        return

    node_id = data['node_id']
    node_blocks = await NodeBlockDAL.read(session, node_id=node_id)

    nodes = await NodeDAL.read(session)
    last_node = nodes[-1]

    if node_id == last_node.id:
        await UserDAL.update(session, user_id=user.id, test_is_finished=True)

    if len(node_blocks) == 0:
        await message.answer('error 38')
        return
    elif len(node_blocks) == 1:
        await state.update_data(last_node_id=node_id, node_id=node_blocks[0].next_node_id)
        if node_blocks[0].block_type == 'text':
            await message.answer(node_blocks[0].content)
            next_node_block_is_text = await NodeBlockDAL.read(
                session, node_id=node_blocks[0].next_node_id, block_type='text'
            )
            if len(next_node_block_is_text) > 0:
                await on_message(message, state, session)
        elif node_blocks[0].block_type == 'input':
            last_node_block = await NodeBlockDAL.read(session, node_id=data['last_node_id'], block_type='text')
            last_node_block_id = last_node_block[0].id
            await AnswerDAL.create(session, answer=message.text, node_block_id=last_node_block_id, user_id=user.id)
            await on_message(message, state, session)
    elif len(node_blocks) > 1:
        await state.update_data(last_node_id=node_id, node_id=node_blocks[0].next_node_id)
        button_node_blocks = []
        text_node_block = None
        for block in node_blocks:
            if block.block_type == 'text':
                text_node_block = block
            elif block.block_type == 'button':
                button_node_blocks.append(block)

        if not text_node_block:
            await message.answer('error 65')
            return

        kb_builder = InlineKeyboardBuilder()
        for button in button_node_blocks:
            kb_builder.button(text=button.content, callback_data=f'node_block_id:{button.id}')

        await message.answer(text=text_node_block.content, reply_markup=kb_builder.as_markup())


@router.callback_query()
async def callback_handler(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    user = await UserDAL.get_user(session, tg_id=str(callback.message.chat.id))

    await callback.message.edit_reply_markup(reply_markup=None)

    last_node_block_id = int(callback.data.split(':')[1])
    last_node_block_list = await NodeBlockDAL.read(session, id=last_node_block_id)

    await state.update_data(last_node_id=last_node_block_list[0].node_id, node_id=last_node_block_list[0].next_node_id)

    await AnswerDAL.create(
        session, answer=last_node_block_list[0].content, node_block_id=last_node_block_id, user_id=user.id
    )

    await on_message(callback.message, state, session)
