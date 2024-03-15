import uvicorn
from fastapi import FastAPI

from video.api.v1.routes.video import video_router

app = FastAPI()

app.include_router(video_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
