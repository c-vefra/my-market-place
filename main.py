from fastapi import FastAPI, Depends, HTTPException, status
from auth import AuthHandler
from app.model import AuthorLogin, Book

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
        "cover": "image1",
        "price": 10000
    },
    {
        "id": 2,
        "title": "Book2",
        "description": "My book2",
        "author": {
            "pseudonym": "author2"
    },
        "cover": "image2",
        "price": 20000
    },
    {
        "id": 3,
        "title": "Book3",
        "description": "My book3",
        "author": {
            "pseudonym": "author3"
    },
        "cover": "image3",
        "price": 30000
    },
]

@app.get(path="/",tags=["test"])
def home():
    return {"":""}

@app.get(path="/books", tags=["Books"])
def get_books():
    return {"data": books}

@app.get(path="/books/{id}", tags=["Books"])
def get_book(id:int):
    if id > len(books):
        return {
            "error": "That book does not exist"
        }
    for book in books:
        if book["id"] == id:
            return {
                "data":book
            }

@app.post('/authors/register', status_code=status.HTTP_201_CREATED)
def authors_register(author_details: AuthorLogin):
    if any(author['pseudonym'] == author_details.pseudonym for author in authors):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='The pseudonym is taken')
    hashed_password = auth_handler.get_password_hash(author_details.password)
    authors.append({
        'pseudonym': author_details.pseudonym,
        'password': hashed_password
    })
    return


@app.post('/authors/login')
def authors_login(author_details: AuthorLogin):
    user = None
    for author in authors:
        if author['pseudonym'] == author_details.pseudonym:
            user = author
            break

    if (user is None) or (not auth_handler.verify_password(author_details.password, user['password'])):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid pseudonym and/or password')
    token = auth_handler.encode_token(user['pseudonym'])
    return { 'token': token }

@app.post(path="/books", dependencies=[Depends(auth_handler.auth_wrapper)], tags=["Books"])
def post_book(book:Book):
    book.id = len(books) + 1
    books.append(book.dict())
    return {
        "info": "book added"
    }

@app.delete(path="/books/{id}", dependencies=[Depends(auth_handler.auth_wrapper)], tags=["Books"])
def delete_book(id:int):
    book = get_book(id)
    print(book["data"])
    if book is not None:
        books.remove(book["data"])
    return {
        "info": "book removed"
    }