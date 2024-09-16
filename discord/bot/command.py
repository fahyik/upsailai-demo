import discord

class TomoCommand:
    def __init__(self, bot, command):
        self.bot = bot
        self.bot.tree.command(name=command, description="Find the perfect product match")(self.match_command)

    async def match_command(self, interaction: discord.Interaction):
        await interaction.channel.create_thread(
            name=f"Find best match product - {interaction.user.display_name}",
            type=discord.ChannelType.public_thread,
            auto_archive_duration=60
        )
        await interaction.response.send_message(
            "Hello! To help me find the perfect product match, please upload a photo of your clothing in this thread or write your requirements.",
            ephemeral=True
        )
