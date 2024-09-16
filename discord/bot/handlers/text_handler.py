from bot.handlers.base_handler import BaseHandler

class TextMessageHandler(BaseHandler):
    async def handle(self, message):
        try:
            await message.channel.send(
                "Please wait a moment while I find the best product recommendations for you."
            )

            user_query = message.content.strip()
            if len(user_query) < 2:
                await message.channel.send(
                    "Could you please provide a photo of your clothing or describe your preferences so I can assist you better?"
                )
                return

            # Invoke the stylist chain without image
            style_suggestions = self.chain_manager.stylist_chain_without_image.invoke({
                "user_query": user_query
            })

            await message.channel.send(style_suggestions['description'])

            # Use the shared process_message method
            await self.process_message(message, style_suggestions, user_query)

        except Exception as e:
            await message.channel.send(
                "Oops! Something went wrong on my end. Please try again in a moment."
            )
            raise e
