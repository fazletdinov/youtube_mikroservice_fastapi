from pydantic import BaseModel, ConfigDict, EmailStr, SecretStr


class CreateUserSchema(BaseModel):
    email: EmailStr
    password: SecretStr


class UpdateUserSchema(BaseModel):
    email: EmailStr | None


class ResponseUserSchema(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True, revalidate_instances="always")


class LoginRequest(BaseModel):
    email: EmailStr
    password: SecretStr
