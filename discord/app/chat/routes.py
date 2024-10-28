from fastapi import APIRouter, status
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel

from .chain import get_stream


chat_router = APIRouter(prefix="/chat")


class ChatRequest(BaseModel):
    streaming: bool
    text: str


@chat_router.post("/", status_code=status.HTTP_200_OK)
async def chat(body: ChatRequest):

    if body.streaming:

        return StreamingResponse(
            get_stream("what would go well with chelsea boots ?"),
            media_type="text/event-stream",
            headers={"Connection": "keep-alive"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(content={"success": True})
