import uvicorn
from fastapi import FastAPI

from users.api.v1.routes.auth import auth_router

app = FastAPI()

app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
