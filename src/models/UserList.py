from pydantic import BaseModel, EmailStr, HttpUrl


class User(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    avatar: HttpUrl


class UserList(BaseModel):
    items: list[User]
    total: int
    page: int
    size: int
    pages: int