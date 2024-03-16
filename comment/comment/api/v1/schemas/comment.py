from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CommentSchemaRequest(BaseModel):
    text: str


class CommentSchemaResponse(BaseModel):
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, revalidate_instances="always")


class CommentSchemaUpdate(BaseModel):
    text: str | None
