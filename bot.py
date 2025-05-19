import os

import discord
import asyncio
import shutil
from discord.ext import commands
from dotenv import load_dotenv
from src import setup_logger

log = setup_logger(__name__)

# --- Environment Variables ---
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
USER_ID = os.getenv("USER_ID")  # temporary

if not DISCORD_TOKEN:
    log.error("DISCORD_BOT_TOKEN not found in environment variables!")
    exit("Discord token not found. Please set DISCORD_BOT_TOKEN in your .env file.")

intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True
intents.messages = True

# --- Bot Initialization ---
bot = commands.Bot(command_prefix="!", intents=intents)

# --- Bot Events ---
@bot.event
async def on_ready():
    log.info(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    log.info('Bot is ready and listening for DMs.')
    
    # if there is a temp_chroma_db folder, move it to chroma_db
    data_path = os.path.join(os.getcwd(), os.getenv("VECTOR_DB_PATH"))
    if os.path.exists(os.path.join(data_path, 'temp_chroma_db')):
        mark_file = os.path.join(data_path, 'temp_chroma_db', '.valid')
        if os.path.isfile(mark_file):
            os.remove(mark_file)
            shutil.rmtree(os.path.join(data_path, 'chroma_db'))
            os.rename(os.path.join(data_path, 'temp_chroma_db'), os.path.join(data_path, 'chroma_db'))
        else:
            log.warning("Found an incomplete temp chroma database, execution will proceed to clear it.")
            shutil.rmtree(os.path.join(data_path, 'temp_chroma_db'))
    
    await load_cogs()
    
    ### temporary, try to find a better way to dm user ###
    user = await bot.fetch_user(USER_ID)
    if user:
        if not user.dm_channel:
            try:
                await user.create_dm()
            except Exception as e:
                log.error(f"Failed to create DM channel for user {user.name} (ID: {user.id}): {e}")
        try:
            message = await user.dm_channel.send("This is a private message from the bot. It will be deleted in 3 seconds.")
            await asyncio.sleep(3)
            await message.delete()
        except Exception as e:
            log.error(f"Failed to send or delete message to user {user.name} (ID: {user.id}): {e}")
    ### end temporary ###


@bot.event
async def on_error(event, *args, **kwargs):
    log.error(f"Unhandled error in event {event}:", exc_info=True)

# TODO Currently unsure how to pass the global config to cogs
# # --- Load Configuration ---
# def load_config():
#     log.info("Loading application configuration...")
#     app_config = AppConfig(
#         personality_config_path="configs/personality.yaml",
#         exception_message_config_path="configs/exception_message.yaml"
#     )
#     log.info("Configuration loaded.")
#     return app_config

# --- Cog Loading ---
async def load_cogs():
    log.info("Attempting to load cogs...")
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('_'):
            cog_name = f'cogs.{filename[:-3]}'
            try:
                await bot.load_extension(cog_name)
            except commands.ExtensionNotFound:
                log.error(f"Cog not found: {cog_name}")
            except commands.ExtensionAlreadyLoaded:
                log.warning(f"Cog already loaded: {cog_name}")
            except commands.NoEntryPointError:
                log.error(f"Cog '{cog_name}' does not have a setup function.")
            except commands.ExtensionFailed as e:
                log.error(f'Failed to load cog {cog_name}: {e.__cause__}', exc_info=True)
            except Exception as e:
                log.error(f"An unexpected error occurred while loading cog {cog_name}: {e}", exc_info=True)
                
    slash = await bot.tree.sync()
    log.info(f'Synced {len(slash)} slash command groups.')


# --- Run Bot ---
if __name__ == "__main__":
    log.info("Starting bot...")
    try:
        bot.run(DISCORD_TOKEN, log_handler=None)
    except discord.LoginFailure:
        log.error("Failed to login to Discord. Please check your bot token.")
    except Exception as e:
        log.critical(f"An error occurred while running the bot: {e}", exc_info=True)