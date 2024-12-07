# @sarkari_student
import asyncio
import importlib
from pyrogram import idle
from plugins import LOGGER, bot as app
from plugins.modules import ALL_MODULES
from plugins.modules.vsp import load_batches_on_start  # Import the function

async def _start():
    try:
        await app.start()
    except Exception as ex:
        LOGGER.error(f"Bot start failed: {ex}")
        quit(1)

    for all_module in ALL_MODULES:
        try:
            importlib.import_module("plugins.modules." + all_module)
            LOGGER.info(f"Module {all_module} imported successfully.")
        except Exception as e:
            LOGGER.error(f"Failed to import module {all_module}: {e}")

    LOGGER.info(f"@{app.username} Started.")
    
    try:
        await load_batches_on_start()
        LOGGER.info("Batches loaded and scheduled.")
    except Exception as e:
        LOGGER.error(f"Error during batch loading: {e}")

    await app.send_message(7224758848, f"**🟢नमस्ते मलिक ! हम जिंदा हो चुके हैं बताइए आपकी क्या आज्ञा है🙏🟠**")
    await idle()

if __name__ == "__main__":
    try:
        asyncio.run(_start())
    except KeyboardInterrupt:
        LOGGER.info("Bot stopped manually.")
