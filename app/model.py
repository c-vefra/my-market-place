from pydantic import BaseModel, Field
from typing import Optional


class AuthorLogin(BaseModel):
    pseudonym:str = Field(
        default=None,
        min_length=3,
        max_length=20
    )
    password:str = Field(
        ...,
        min_length=8
    )

class Author(BaseModel):
    pseudonym:str = Field(
        default=None,
        min_length=3,
        max_length=20
    )


class Book(BaseModel):
    id: int = Field(...)
    title:str = Field(
        ...,
        min_length=3,
        max_length=50
    )
    description:str = Field(
        default=None,
        min_length=3,
        max_length=50
    )
    author:Author = Field(...)
    cover:Optional[str]
    price:int = Field(
        default=None,
        ge=0
    )