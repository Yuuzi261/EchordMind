import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from src import setup_logger

log = setup_logger(__name__)

# --- Environment Variables ---
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

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
    await load_cogs()

@bot.event
async def on_error(event, *args, **kwargs):
    log.error(f"Unhandled error in event {event}:", exc_info=True)

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


# --- Run Bot ---
if __name__ == "__main__":
    log.info("Starting bot...")
    try:
        bot.run(DISCORD_TOKEN, log_handler=None)
    except discord.LoginFailure:
        log.error("Failed to login to Discord. Please check your bot token.")
    except Exception as e:
        log.critical(f"An error occurred while running the bot: {e}", exc_info=True)