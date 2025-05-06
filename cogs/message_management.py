import discord
from discord import app_commands
from discord.ext import commands
from src import setup_logger
from core import Cog_Extension

log = setup_logger(__name__)

class MessageManagementCog(Cog_Extension):

    clear_group = app_commands.Group(name='clear', description='Clear something')

    @clear_group.command(name="history")
    @app_commands.rename(n="delete_amount")
    async def clear_history(self, interaction: discord.Interaction, n: int = 10):
        """Delete the last n of the bot's messages in the DM channel

        Parameters
        -----------
        n: int
            The number of messages to delete.
        """
        await interaction.response.defer(ephemeral=True)

        if interaction.user.dm_channel is None:
            await interaction.user.create_dm()

        dm_channel = interaction.user.dm_channel

        if n <= 0:
            await interaction.followup.send("Please enter a positive integer for the number of messages to delete.", ephemeral=True)
            return

        if n > 500:
            await interaction.followup.send("You can only specify up to 500 robot messages to be deleted at a time.", ephemeral=True)
            return

        messages_to_delete = []
        bot_messages_found = 0
        errors_during_fetch = []

        try:
            async for message in dm_channel.history(limit=None):
                if message.author == self.bot.user:
                    messages_to_delete.append(message)
                    bot_messages_found += 1
                    if bot_messages_found >= n:
                        break
        except Exception as e:
            errors_during_fetch.append(f"Error occurred while fetching message history: {e}")
            await interaction.followup.send(f"An error occurred, unable to retrieve message history: {e}", ephemeral=True)
            return

        if not messages_to_delete:
            response_text = f"No recent {n} bot messages found in history."
            await interaction.followup.send(response_text, ephemeral=True)
            return

        deleted_count = 0
        errors_during_deletion = []

        for msg in messages_to_delete:
            try:
                await msg.delete()
                deleted_count += 1
            except discord.Forbidden:
                errors_during_deletion.append(f"Failed to delete a message (ID: {msg.id}, possibly lacking permissions).")
            except discord.HTTPException as e:
                errors_during_deletion.append(f"HTTP error occurred while deleting a message (ID: {msg.id}): {e}")
            except Exception as e:
                errors_during_deletion.append(f"An unexpected error occurred while deleting a message (ID: {msg.id}): {e}")

        response_text = f"Attempted to delete {len(messages_to_delete)} bot messages found (target was {n})."
        if deleted_count > 0:
            response_text += f"\nSuccessfully deleted {deleted_count} messages."
        if errors_during_deletion:
            response_text += "\n\nThe following issues occurred during deletion:\n" + "\n".join(errors_during_deletion)

        await interaction.followup.send(response_text, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(MessageManagementCog(bot))
    log.info("MessageManagementCog added successfully.")