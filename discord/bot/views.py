import base64
import io

import discord
from discord.ui import View


class Carousel(View):
    def __init__(self, products, thread):
        super().__init__(timeout=180)  # Timeout after 3 minutes of inactivity
        self.products = products
        self.current = 0
        self.thread = thread
        self.message = None  # Will hold the message object after sending

    async def update_embed(self, interaction=None):
        product = self.products[self.current]

        # Decode the base64 image
        image_data = base64.b64decode(product['image_base64'])
        image_file = discord.File(io.BytesIO(image_data), filename='image.png')

        embed = discord.Embed(
            title=product['name'],
            description=product['description']
        )
        embed.set_image(url=f'attachment://image.png')
        embed.set_footer(text=f"Product {self.current + 1}/{len(self.products)}")

        if interaction is None:
            # Initial message send
            self.message = await self.thread.send(embed=embed, file=image_file, view=self)
        else:
            # Edit existing message
            await interaction.message.edit(embed=embed, attachments=[image_file], view=self)
            await interaction.response.defer()

    @discord.ui.button(label='◀️', style=discord.ButtonStyle.primary)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current > 0:
            self.current -= 1
            await self.update_embed(interaction)
        else:
            await interaction.response.defer()  # Do nothing if at the first product

    @discord.ui.button(label='▶️', style=discord.ButtonStyle.primary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current < len(self.products) - 1:
            self.current += 1
            await self.update_embed(interaction)
        else:
            await interaction.response.defer()  # Do nothing if at the last product
