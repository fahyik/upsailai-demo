from app.core.config import settings
import json
from chains.chain_manager import ChainManager
from langchain_openai import ChatOpenAI
from langchain_core.messages.ai import AIMessageChunk

manager = ChainManager(
    persist_directory="/Users/fahyik/Dev/upsailai-demo/chroma_db",
    docstore_path="/Users/fahyik/Dev/upsailai-demo/doc_store",
    openai_token=settings["OPENAI_API_KEY"],
)


from langchain.callbacks.base import BaseCallbackHandler


class RawResponseHandler(BaseCallbackHandler):

    def on_chat_model_start(self, serialized, messages, **kwargs):
        print(serialized)

    def on_llm_new_token(self, token: str, chunk, **kwargs):
        print(token)

    # def on_llm_end(self, response, **kwargs):
    #     self.raw_response = response.llm_output["text"]


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, AIMessageChunk):
            return obj.__dict__  # Convert to dict or define your transformation
        return super().default(obj)


async def get_stream(query):

    print(query)

    events = manager.stylist_chain_without_image.astream_events(query, version="v2")

    async for event in events:

        # print(json.dumps(event, cls=CustomEncoder, indent=4))

        if event["event"] == "on_chat_model_stream":

            message = f"0:\"{event['data']['chunk'].content}\"\n"

            # message = (
            #     f"data: {json.dumps({'text': event['data']['chunk'].content})}\n\n"
            # )
            yield message.encode("utf-8")  # Encode as bytes for StreamingResponse
