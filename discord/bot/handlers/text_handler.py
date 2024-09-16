from bot.handlers.base_handler import BaseHandler
from bot.views import Carousel
from chains.utils.formatter import format_docs


class TextMessageHandler(BaseHandler):
    async def handle(self, message):
        try:
            await message.channel.send("Please wait a moment while I find the best product recommendations for you.")
            user_query = message.content.strip()
            if len(user_query) < 2:
                await message.channel.send("Could you please provide a photo of your clothing or describe your preferences so I can assist you better?")
                return

            style_suggestions = self.chain_manager.stylist_chain_without_image.invoke({"user_query": user_query})
            retrieved_products, retrieved_docs = self.chain_manager.retrieve_products(style_suggestions['clothes'])
            question = self.chain_manager.build_question(style_suggestions, user_query)
            recommend_products = self.chain_manager.sale_assistant_chain.invoke({
                "context": format_docs(retrieved_docs.values()),
                "question": question,
            })

            products = self.chain_manager.organize_products(recommend_products, retrieved_products)
            await self.display_products(message, products)
        except Exception as e:
            await message.channel.send(f"Oops! Something went wrong on my end. Please try again in a moment.\n{e}")
            raise e

    async def display_products(self, message, products):
        for category, selected_products in products.items():
            await message.channel.send(f"I've found some {category.lower()} items you might like:")
            product_list = list(selected_products.values())
            view = Carousel(product_list, message.channel)
            await view.update_embed()
