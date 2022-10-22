import logging
from datetime import timedelta, datetime

from aiogram import Bot, Dispatcher, executor
from aiogram import types

import config

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(content_types=["new_chat_members"])
async def handler_new_member(message):
    await bot.send_message(message.chat.id, f"Привет @{message.from_user.username}!"
                                            f"Добро пожаловать в Ukrainian Crypto | Chat.")


@dp.message_handler(commands=['mute'], commands_prefix='/', is_chat_admin=True)
async def mute(message):
    name1 = message.from_user.get_mention(as_html=True)
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение!")
        return
    muteint = int(message.text.split()[1])
    if True:
        dt = datetime.now() + timedelta(hours=muteint)
        timestamp = dt.timestamp()
        await bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id,
                                       permissions=types.ChatPermissions(False), until_date=int(timestamp))
        await message.reply(
            f' | <b>Решение было принято:</b> {name1}\n | <b>Нарушитель:</b> <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>\n⏰ | <b>Срок наказания:</b> {muteint} минут',
            parse_mode='html')


@dp.message_handler(commands=['ban'], commands_prefix='/', is_chat_admin=True)
async def mute(message):
    name1 = message.from_user.get_mention(as_html=True)
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение!")
        return
    else:
        await bot.ban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id,
                                  revoke_messages=True)
        await message.reply(
            f' | <b>Решение было принято:</b> {name1}\n | <b>Нарушитель:</b> <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>\n⏰ | <b>Срок наказания:</b> Навсегда',
            parse_mode='html')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
