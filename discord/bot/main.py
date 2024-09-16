# app/main.py

from bot.bot import TomoBot
from bot.config import TOKEN

if __name__ == "__main__":
    bot = TomoBot()
    bot.run(TOKEN)
