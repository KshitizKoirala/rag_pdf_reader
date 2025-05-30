from pydantic import BaseModel, EmailStr


class LoginCredentials(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    API_KEY: str
