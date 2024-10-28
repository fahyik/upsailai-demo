from app.chat.routes import chat_router
from app.utils.logging import setup_logging
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Set up logging configuration
setup_logging()

app = FastAPI(
    title="Production Grade FastAPI Server",
    description="A simple production-ready FastAPI server",
    version="1.0.0",
)


@app.get("/ready")
def ready():
    return JSONResponse(content={"success": True, "status": "ready"})


# Include API router
app.include_router(chat_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    # Any startup tasks (e.g., connecting to database)
    pass


@app.on_event("shutdown")
async def shutdown_event():
    # Any shutdown tasks (e.g., closing database connection)
    pass
