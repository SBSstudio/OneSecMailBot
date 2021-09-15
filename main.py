import logging
from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN
import keyboard as kb
from onesec_api import Mailbox
import json
import asyncio

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(content_types=['text'])
async def texthandler(m: types.Message):
    if m.text != 'Receive mail':
        await m.answer(f'welcome, {m.from_user.mention}\nThis bot is designed to receive temporary mail messages quickly.  Click the button below', reply_markup=kb.menu)
    elif m.text == 'Receive mail':
        ma = Mailbox('')
        email = f'{ma._mailbox_}@1secmail.com'
        await m.answer(f'➕ Here is your email: {email}\nSend a message.\nMail is checked automatically, every 4 seconds, if a new message arrives, we will notify you!\nNote: You can only receive one message - per email')
        while True:
            mb = ma.filtred_mail()
            if isinstance(mb, list):
                mf = ma.mailjobs('read',mb[0])
                js = mf.json()
                fromm = js['from']
                theme = js['subject']
                mes = js['textBody']
                await m.answer(f'💬 New message:\nfrom</b>: {fromm}\n<b>Issue</b>: {theme}\n<b>Message</b>: {mes}', reply_markup=kb.menu, parse_mode='HTML')
                break
            else:
                pass
            await asyncio.sleep(4)
 

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
