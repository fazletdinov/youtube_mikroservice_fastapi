from pydantic import BaseModel, ConfigDict


class CreateVideoSchema(BaseModel):
    title: str
    description: str
    file: str
    image: str


class UpdateVideoSchema(BaseModel):
    title: str | None
    description: str | None
    file: str | None
    image: str | None


class ResponseVideoSchema(BaseModel):
    id: int
    title: int
    description: str
    file: str
    image: str

    model_config = ConfigDict(from_attributes=True, revalidate_instances="always")
