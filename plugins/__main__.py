# @sarkari_student
import asyncio
import importlib
from pyrogram import idle
from plugins import LOGGER, bot as app
from plugins.modules import ALL_MODULES
from plugins.modules.vsp import load_batches_on_start  # Import the function

async def _start():
    try:
        # Start the Pyrogram bot
        await app.start()
    except Exception as ex:
        LOGGER.error(ex)
        quit(1)

    # Dynamically import all modules
    for all_module in ALL_MODULES:
        importlib.import_module("plugins.modules." + all_module)

    LOGGER.info(f"@{app.username} Started.")

    try:
        # Call load_batches_on_start to initialize scheduled batches
        await load_batches_on_start()
        LOGGER.info("Batches loaded and scheduled.")
    except Exception as e:
        LOGGER.error(f"Error during batch loading: {e}")

    # Notify the owner
    await app.send_message(
        7224758848,
        "**🟢नमस्ते मलिक ! हम जिंदा हो चुके हैं बताइए आपकी क्या आज्ञा है🙏🟠**"
    )

    # Keep the bot running
    await idle()

async def main():
    # Run the bot and clean up on exit
    try:
        await _start()
    finally:
        await app.stop()
        LOGGER.info("Bot stopped.")

if __name__ == "__main__":
    asyncio.run(main())
