from fastapi import FastAPI
from app.controllers.parser import router as parse_router
from app.utils.helpers import setup_logger

logger = setup_logger(__name__)

app = FastAPI()
app.include_router(parse_router)

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI application...")
    uvicorn.run(app, host="127.0.0.1", port=3000)