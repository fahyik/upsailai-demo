# app/bot.py

import discord
from discord.ext import commands

from bot.config import OPENAI_TOKEN, PERSIST_DIR, DOCSTORE_PATH, COMMAND_NAME
from bot.healthcheck import start_http_health_check
from bot.handlers.image_handler import ImageMessageHandler
from bot.handlers.text_handler import TextMessageHandler
from bot.command import TomoCommand
from chains.chain_manager import ChainManager

class TomoBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)

        self.chain_manager = ChainManager(
            persist_directory=PERSIST_DIR,
            docstore_path=DOCSTORE_PATH,
            openai_token=OPENAI_TOKEN
        )

        # Initialize handlers
        self.image_handler = ImageMessageHandler(self.chain_manager)
        self.text_handler = TextMessageHandler(self.chain_manager)
        self.tomo_command = TomoCommand(self, COMMAND_NAME)

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        start_http_health_check(self, port=8000, bot_max_latency=0.5)
        print(f"Logged in as {self.user}")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if isinstance(message.channel, discord.Thread) and message.channel.owner == self.user:
            if message.attachments:
                for attachment in message.attachments:
                    if attachment.content_type and attachment.content_type.startswith('image/'):
                        await self.image_handler.handle(message, attachment)
                    else:
                        await message.channel.send(
                            f"Sorry, I can only process image files. The file type you've uploaded ({attachment.content_type}) isn't supported. Please upload a valid image of your clothing.")
            else:
                await self.text_handler.handle(message)