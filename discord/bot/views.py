import discord
from discord.ui import View, Button


class InitialView(View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Complete the look", style=discord.ButtonStyle.primary, custom_id="complete_look")
    async def complete_look(self, button: discord.ui.Button, interaction: discord.Interaction):
        embeds = [
            discord.Embed(title=fit['name'], description=fit['description']).set_image(url=fit["image"])
            for fit in fits
        ]
        await interaction.response.send_message("Here are the complete clothes:", view=StyleView(fits, "complete"), embeds=embeds)

    @discord.ui.button(label="Find similar clothes", style=discord.ButtonStyle.red, custom_id="find_similar")
    async def find_similar(self, button: discord.ui.Button, interaction: discord.Interaction):
        embeds = [
            discord.Embed(title=similar['name'], description=similar['description']).set_image(url=similar["image"])
            for similar in similars
        ]
        await interaction.response.send_message("Here are similar clothes:", view=StyleView(similars, "similar"), embeds=embeds)