from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, Query, status
from auth import AuthHandler
from app.model import AuthorBase, AuthorRegister, Book

app=FastAPI()

auth_handler = AuthHandler()
authors = []

books = [
    {
        "id": 1,
        "title": "Book1",
        "description": "My book1",
        "author": {
            "pseudonym": "author1"
    },
        "cover": 254000,
        "price": 10000
    },
    {
        "id": 2,
        "title": "Book2",
        "description": "My book2",
        "author": {
            "pseudonym": "author2"
    },
        "cover": 200000,
        "price": 20000
    },
    {
        "id": 3,
        "title": "Book3",
        "description": "My book3",
        "author": {
            "pseudonym": "author3"
    },
        "cover": 500000,
        "price": 30000
    },
]

@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
    tags=["Authors"]
)
def home():
    """
    **Authors**

    This path operation shows the authors

    Parameters:
        -

    Returns a json with the authors information

        - pseudonym

        - cipher password

    """
    return {"author":authors}

@app.post(
    path="/authors/register",
    status_code=status.HTTP_201_CREATED,
    tags=["Authors"]
)
def authors_register(author_details: AuthorRegister):
    """
    **Authors Register**

    This path operation registers an author

    Parameters:

        -

    Returns a json with a success message of registered
    """
    if any(author["pseudonym"] == author_details.pseudonym for author in authors):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The pseudonym is taken"
        )
    hashed_password = auth_handler.get_password_hash(author_details.password)
    authors.append({
        "pseudonym": author_details.pseudonym,
        "password": hashed_password
    })
    return {"message":"registered"}


@app.post(
    path="/authors/login",
    status_code=status.HTTP_201_CREATED,
    tags=["Authors"]
)
def authors_login(author_details: AuthorRegister):
    """
    **Authors Login**

    This path operation logs in an author

    Parameters:

        -

    Returns a json with a token
    """
    user = None
    for author in authors:
        if author["pseudonym"] == author_details.pseudonym:
            user = author
            break

    if (user is None) or (not auth_handler.verify_password(author_details.password, user["password"])):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid pseudonym and/or password"
        )
    token = auth_handler.encode_token(user["pseudonym"])
    return {"token": token}

@app.get(
    path="/books",
    status_code=status.HTTP_200_OK,
    tags=["Books"]
)
def get_books(id:Optional[int]=Query(default=None)):
    """
    **Shows the books**

    This path operation shows the books collection

    Parameters:

        - id (optional)


    Returns a json with the books
    """
    if id:
        if id <= len(books):
            for book in books:
                if book["id"] == id:
                    return {"data":book}
        elif id > len(books):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The Book does not exist"
            )
    return {"data": books}

@app.get(
    path="/books/{id}",
    status_code=status.HTTP_200_OK,
    tags=["Books"]
)
def get_book(id:int):
    """
    **Shows one book**

    This path operation shows one book

    Parameters:

        - id


    Returns a json with the book information
    """
    if id > len(books):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The Book does not exist"
        )
    for book in books:
        if book["id"] == id:
            return {"data":book}

@app.post(
    path="/books",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(auth_handler.auth_wrapper)],
    tags=["Books"]
)
def post_book(book:Book, author: AuthorBase):
    """
    **Post a book**

    This path operation posts a book

    Parameters:

        -

    Returns a json with a success message of book added
    """
    if author.pseudonym != "_Darth Vader_":
        book.author.pseudonym = author.pseudonym
        book_id = books[book.id-1]["id"]
        book.id = book_id + 1
        books.append(book.dict())
        return {"info":"book added"}
    else:
        raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="This author can not publish this book"
    )

@app.delete(
    path="/books/{id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(auth_handler.auth_wrapper)],
    tags=["Books"]
)
def delete_book(id:int, author: AuthorBase):
    """
    **Delete a book**

    This path operation deletes a book

    Parameters:

        - id

    Returns a json with a success message of book removed
    """
    book = get_book(id)
    if book["data"]["author"]["pseudonym"] == author.pseudonym:
        print(book["data"])
        if book is not None:
            books.remove(book["data"])
        return {"info":"book removed"}
    else:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="This author can not delete this book"
    )

