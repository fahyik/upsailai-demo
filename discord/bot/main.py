import discord

from rag.chain import build_openai_chain

from .config import TOKEN, OPENAI_TOKEN, PERSIST_DIR, DOCSTORE_PATH
from .healthcheck import HealthCheckDiscordClient


intents = discord.Intents.default()
intents.message_content = True

client = HealthCheckDiscordClient(intents=intents)

rag_chain = None

@client.event
async def on_ready():
    global rag_chain

    rag_chain = build_openai_chain(
        PERSIST_DIR,
       DOCSTORE_PATH,
        OPENAI_TOKEN,
    )

    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message: discord.Message):
    if message.content.startswith('/stylist'):
        question = message.content[len('/stylist'):].strip()
        # Use the pre-initialized RAG chain to generate a response
        response = rag_chain.invoke(question)

        # Send the response back to the user in the DM
        await message.channel.send(response)

client.run(TOKEN)
