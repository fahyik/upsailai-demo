import base64
import json
import os

import discord
from discord.ext import commands
from langchain_openai import ChatOpenAI

from rag.chain import load_retriever, build_chain, build_stylist_chain

from .config import TOKEN, OPENAI_TOKEN, PERSIST_DIR, DOCSTORE_PATH
from .healthcheck import start_http_health_check
from .views import Carousel

os.environ["OPENAI_API_KEY"] = OPENAI_TOKEN

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

retriever = None
rag_chain = None
stylist_chain = None

@bot.event
async def on_ready():
    global retriever
    global rag_chain
    global stylist_chain

    retriever = load_retriever(
        persist_directory=PERSIST_DIR,
        docstore_path=DOCSTORE_PATH
    )

    llm_4o_mini = ChatOpenAI(model="gpt-4o-mini")
    llm_4o = ChatOpenAI(model="gpt-4o")

    rag_chain = build_chain(retriever, llm_4o_mini)
    stylist_chain = build_stylist_chain(llm_4o)

    start_http_health_check(bot, port=8000, bot_max_latency=0.5)

    await bot.tree.sync()
    print(f"Logged in as {bot.user}")


@bot.tree.command(name="tomo", description="Find the perfect product match")
async def match_command(interaction: discord.Interaction):

    # Create a thread from the interaction message
    thread = await interaction.channel.create_thread(
        name=f"Find best match product - {interaction.user.display_name}",
        type=discord.ChannelType.public_thread,
        auto_archive_duration=60  # Auto-archive after 60 minutes of inactivity
    )

    # Send an initial response to acknowledge the command
    await interaction.response.send_message("Please post your clothes photo in thread", ephemeral=True)


@bot.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == bot.user:
        return

    # Check if the message is in a thread created by the bot
    if isinstance(message.channel, discord.Thread) and message.channel.owner == bot.user and message.content:
        # Check if the message has attachments
        if message.attachments:
            for attachment in message.attachments:
                # Only process image files
                if attachment.content_type and attachment.content_type.startswith('image/'):
                    await handle_image_message(message, attachment)
                else:
                    await message.channel.send(f"Unsupported file type: {attachment.content_type}")
        else:
            await message.channel.send("Please attach an image.")


async def handle_image_message(message, attachment):
    try:
        # Download the image into memory
        image_bytes = await attachment.read()

        # Encode the image in base64
        base64_encoded = base64.b64encode(image_bytes).decode('utf-8')

        # Get the image's MIME type
        mime_type = attachment.content_type  # e.g., 'image/jpeg'

        # Format the message
        formatted_message = f"data:{mime_type};base64,{base64_encoded}"

        await message.channel.send("Just a moment! Tomo is searching for the perfect product match for you.")

        style_suggestions = stylist_chain.invoke({"image_url": formatted_message})
        products = {}
        for query in style_suggestions['clothes']:
            docs = retriever.invoke(query)
            for doc in docs:
                product = json.loads(doc.page_content)
                if len(product['image_encodings']) == 0:
                    continue
                products[product['url']] = {
                    'name': product['title'],
                    'description': product['description'],
                    'image_base64': product['image_encodings'][-1],  # Replace with actual base64 string
                }
        product_list = list(products.values())

        # await message.channel.send(style_suggestions['description'])
        view = Carousel(product_list, message.channel)
        await view.update_embed()
    except Exception as e:
        await message.channel.send(f"An error occurred: {e}")
        raise e


bot.run(TOKEN)
