import json
from bot.views import Carousel
from chains.utils.formatter import format_docs
from chains.chain_manager import ChainManager


class BaseHandler:
    def __init__(self, chain_manager: ChainManager):
        self.chain_manager = chain_manager

    async def process_message(self, message, style_suggestions, user_query):
        try:
            # Retrieve products based on style suggestions
            retrieved_products, retrieved_docs = self.chain_manager.retrieve_products(style_suggestions['clothes'])

            # Build the question for the sales assistant chain
            question = self.chain_manager.build_question(style_suggestions, user_query)

            # Invoke the sales assistant chain
            recommend_products = self.chain_manager.sale_assistant_chain.invoke({
                "context": format_docs(retrieved_docs.values()),
                "question": question,
            })

            # Organize the recommended products
            products = self.chain_manager.organize_products(recommend_products, retrieved_products)

            # Display the products
            await self.display_products(message, products)

        except Exception as e:
            await message.channel.send(
                "Oops! Something went wrong on my end. Please try again in a moment."
            )
            # Optionally log the exception here
            raise e  # Re-raise the exception if you have logging mechanisms

    async def display_products(self, message, products):
        for category, selected_products in products.items():
            await message.channel.send(
                f"I've found some {category.lower()} items you might like:"
            )
            product_list = list(selected_products.values())
            view = Carousel(product_list, message.channel)
            await view.update_embed()
