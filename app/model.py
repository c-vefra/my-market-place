from pydantic import BaseModel, Field
from typing import Optional


class AuthorBase(BaseModel):
    pseudonym:str = Field(
        default=None,
        min_length=3,
        max_length=20,
        example="sr.x"
    )

class AuthorRegister(AuthorBase):
    password:str = Field(
        ...,
        min_length=8,
        example="password123"
    )

class Author(AuthorBase):
    pass


class Book(BaseModel):
    id: int = Field(...)
    title:str = Field(
        ...,
        min_length=3,
        max_length=50,
        example="My new book"
    )
    description:str = Field(
        default=None,
        min_length=3,
        max_length=50,
        example="This is my new book"
    )
    author:Author = Field(...)
    cover:Optional[bytes]
    price:int = Field(
        default=None,
        ge=0,
        example=20000
    )