import asyncio
import importlib

from pyrogram import idle

import config
from config import BANNED_USERS
from ChampuMusic import HELPABLE, LOGGER, app, userbot
from ChampuMusic.core.call import Champu
from ChampuMusic.plugins import ALL_MODULES
from ChampuMusic.utils.database import get_banned_users, get_gbanned


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER("ChampuMusic").error(
            "Assistant client variables not defined, exiting..."
        )
        return

    if not config.SPOTIFY_CLIENT_ID and not config.SPOTIFY_CLIENT_SECRET:
        LOGGER("ChampuMusic").warning(
            "No Spotify vars defined. Your bot won't be able to play Spotify queries..."
        )

    # Load banned users
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception:
        pass

    # Load plugins
    for all_module in ALL_MODULES:
        imported_module = importlib.import_module(all_module)
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                HELPABLE[imported_module.__MODULE__.lower()] = imported_module
    LOGGER("ChampuMusic.plugins").info("Successfully imported modules...")

    # Start assistant
    await userbot.start()

    # Start main bot voice handler
    await Champu.start()
    await Champu.decorators()
    LOGGER("ChampuMusic").info("Successfully started")

    await idle()