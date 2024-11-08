from typing import List, Optional, Union

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, HttpUrl

from .chain import get_recommended_products, get_stream, manager


# Define the model for each message content (text or image)
class MessageContent(BaseModel):
    type: str  # This will be either "text" or "image_url"
    text: Optional[str] = None  # Only present when type is "text"
    image_url: Optional[str] = None  # Only present when type is "image_url"


# Define the model for a message, which is a list of content items
class Message(BaseModel):
    role: str  # e.g., "user"
    content: Union[List[MessageContent], str]


# Define the top-level request model
class ChatRequest(BaseModel):
    messages: Optional[List[Message]] = None
    stream: bool


chat_router = APIRouter(prefix="/chat")


@chat_router.post("", status_code=status.HTTP_200_OK)
async def chat(request: Request, body: ChatRequest):
    b = await request.body()
    print(b)

    if body.stream:

        stream = get_stream(
            "what would go well with chelsea boots ? return me a json object with the shape {'answer': 'your answer'} without markdown formatting"
        )

        return StreamingResponse(
            stream,
            media_type="text/event-stream",
            headers={"Connection": "keep-alive"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={
            "success": True,
            "data": manager.stylist_chain_without_image.invoke(
                "what would go well with chelsea boots ?"
            ),
        }
    )


@chat_router.post("/recommendations", status_code=status.HTTP_200_OK)
async def chatProductRecommendations(request: Request):
    b = await request.json()

    print(b)

    return JSONResponse(
        content={
            "success": True,
            "data": await get_recommended_products(
                b["recommendedProducts"],
                b["stylistExplanation"],
                b["customerStyle"],
                b["customerQuery"],
            ),
        }
    )
