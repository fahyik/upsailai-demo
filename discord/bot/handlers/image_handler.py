import base64

from bot.handlers.base_handler import BaseHandler

class ImageMessageHandler(BaseHandler):
    async def handle(self, message, attachment):
        try:
            # Download the image into memory
            image_bytes = await attachment.read()

            # Encode the image in base64
            base64_encoded = base64.b64encode(image_bytes).decode('utf-8')

            # Get the image's MIME type
            mime_type = attachment.content_type  # e.g., 'image/jpeg'

            # Format the image data
            formatted_message = f"data:{mime_type};base64,{base64_encoded}"

            await message.channel.send(
                "Please wait a moment while I find the best product recommendations for you."
            )

            user_query = message.content.strip() or "Please suggest the best matching style based on the given clothes"

            # Invoke the stylist chain with image
            style_suggestions = self.chain_manager.stylist_chain_with_image.invoke({
                "image_url": formatted_message,
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
