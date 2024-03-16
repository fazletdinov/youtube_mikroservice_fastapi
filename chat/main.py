import uvicorn
from fastapi import FastAPI

# from comment.api.v1.routes.comment import comment_router

app = FastAPI()

# app.include_router(comment_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
