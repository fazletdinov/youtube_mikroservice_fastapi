from pydantic import BaseModel, ConfigDict

from likes.database.models.likes import Type


class ReactionSchemaRequest(BaseModel):
    type_reaction: Type


class ReactionSchemaResponse(BaseModel):
    type_reaction: Type

    model_config = ConfigDict(from_attributes=True, revalidate_instances="always")


class ReactionSchemaUpdate(BaseModel):
    type_reaction: Type | None
