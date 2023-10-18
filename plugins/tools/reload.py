import asyncio

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message

from Bikash.config import BANNED_USERS, MUSIC_BOT_NAME, adminlist, lyrical
from Bikash.Bgt import get_command
from Bikash import app
from Bikash.core.call import Bikashh
from Bikash.misc import db
from Bikash.utils.database import get_authuser_names, get_cmode
from Bikash.utils.decorators import (ActualAdminCB, AdminActual,
                                         language)
from Bikash.utils.formatters import alpha_to_int

### Multi-Lang Commands
RELOAD_COMMAND = get_command("RELOAD_COMMAND")
RESTART_COMMAND = get_command("RESTART_COMMAND")


@app.on_message(
    filters.command(RELOAD_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@language
async def reload_admin_cache(client, message: Message, _):
    try:
        chat_id = message.chat.id
        admins = await app.get_chat_members(
            chat_id, filter="administrators"
        )
        authusers = await get_authuser_names(chat_id)
        adminlist[chat_id] = []
        for user in admins:
            if user.can_manage_voice_chats:
                adminlist[chat_id].append(user.user.id)
        for user in authusers:
            user_id = await alpha_to_int(user)
            adminlist[chat_id].append(user_id)
        await message.reply_text(_["admin_20"])
    except:
        await message.reply_text(
            "𝐑𝐄𝐋𝐎𝐑𝐃 𝐊𝐀𝐑 𝐌𝐄𝐑𝐈 𝐉𝐀𝐀𝐍."
        )


@app.on_message(
    filters.command(RESTART_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@AdminActual
async def restartbot(client, message: Message, _):
    mystic = await message.reply_text(
        f"𝐒𝐀𝐁𝐀𝐀𝐑 𝐊𝐀𝐑 𝐑𝐄𝐒𝐓𝐀𝐑𝐓 𝐇𝐎 𝐑𝐇𝐀 {MUSIC_BOT_NAME} 𝐀𝐃𝐃 𝐊𝐀𝐑𝐋𝐄 𝐁𝐑𝐎 𝐎𝐏 𝐁𝐎𝐓 𝐇𝐔."
    )
    await asyncio.sleep(1)
    try:
        db[message.chat.id] = []
        await Bikashh.stop_stream(message.chat.id)
    except:
        pass
    chat_id = await get_cmode(message.chat.id)
    if chat_id:
        try:
            await app.get_chat(chat_id)
        except:
            pass
        try:
            db[chat_id] = []
            await Bikashh.stop_stream(chat_id)
        except:
            pass
    return await mystic.edit_text(
        f"👅☠️𝐇𝐎 𝐆𝐘𝐀 𝐑𝐄𝐒𝐓𝐀𝐑𝐓 𝐏𝐋𝐀𝐘 𝐊𝐀𝐑𝐋𝐄 𝐁𝐎𝐇𝐎𝐓 𝐌𝐀𝐑 𝐑𝐇𝐀 𝐓𝐇𝐀 🙈 𝐒𝐎𝐍𝐆 𝐒𝐔𝐍𝐍𝐄 𝐊𝐄 𝐋𝐈𝐘𝐄🙈❤ {MUSIC_BOT_NAME} ☹️𝐀𝐃𝐃 𝐊𝐀𝐑𝐋𝐄 𝐁𝐑𝐎 𝐎𝐏 𝐁𝐎𝐓 𝐇𝐔🥺..."
    )


@app.on_callback_query(filters.regex("close") & ~BANNED_USERS)
async def close_menu(_, CallbackQuery):
    try:
        await CallbackQuery.message.delete()
        await CallbackQuery.answer()
    except:
        return


@app.on_callback_query(filters.regex("close") & ~BANNED_USERS)
async def close_menu(_, CallbackQuery):
    try:
        await CallbackQuery.message.delete()
        await CallbackQuery.answer()
    except:
        return


@app.on_callback_query(
    filters.regex("stop_downloading") & ~BANNED_USERS
)
@ActualAdminCB
async def stop_download(client, CallbackQuery: CallbackQuery, _):
    message_id = CallbackQuery.message.message_id
    task = lyrical.get(message_id)
    if not task:
        return await CallbackQuery.answer(
            "𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐂𝐨𝐦𝐩𝐥𝐞𝐭𝐞𝐝.", show_alert=True
        )
    if task.done() or task.cancelled():
        return await CallbackQuery.answer(
            "𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐞𝐝 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐂𝐨𝐦𝐩𝐥𝐞𝐭𝐞𝐝 𝐎𝐫 𝐂𝐚𝐧𝐜𝐞𝐥𝐥𝐞𝐝.",
            show_alert=True,
        )
    if not task.done():
        try:
            task.cancel()
            try:
                lyrical.pop(message_id)
            except:
                pass
            await CallbackQuery.answer(
                "𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐂𝐚𝐧𝐜𝐞𝐥.", show_alert=True
            )
            return await CallbackQuery.edit_message_text(
                f"𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐏𝐫𝐨𝐜𝐞𝐬𝐬 𝐂𝐚𝐧𝐜𝐞𝐥 𝐁𝐲 {CallbackQuery.from_user.mention}"
            )
        except:
            return await CallbackQuery.answer(
                "𝐅𝐚𝐢𝐥𝐞𝐝 𝐓𝐨 𝐂𝐚𝐧𝐜𝐞𝐥 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠...", show_alert=True
            )
    await CallbackQuery.answer(
        "𝐅𝐚𝐢𝐥𝐞𝐝 𝐓𝐨 𝐑𝐞𝐜𝐨𝐠𝐧𝐢𝐳𝐞 𝐓𝐡𝐞 𝐎𝐧 𝐆𝐨𝐢𝐧𝐠  𝐓𝐚𝐬𝐤.", show_alert=True
    )
