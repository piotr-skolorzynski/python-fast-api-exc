from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {"title": "Diuna", "author": "Frank Herbert", "category": "Sci-Fi"},
    {
        "title": "Wiedźmin: Ostatnie życzenie",
        "author": "Andrzej Sapkowski",
        "category": "Fantasy",
    },
    {"title": "Hobbit", "author": "J.R.R. Tolkien", "category": "Fantasy"},
    {
        "title": "Morderstwo w Orient Expressie",
        "author": "Agatha Christie",
        "category": "Kryminał",
    },
    {"title": "Rok 1984", "author": "George Orwell", "category": "Dystopia"},
    {
        "title": "Cień wiatru",
        "author": "Carlos Ruiz Zafón",
        "category": "Literatura piękna",
    },
]


@app.get("/books")
async def get_books():  # w fast api async jest dodawany automatycznie, ale można go dodać ręcznie
    return BOOKS


# endpoint z parametrami tak żeby np pobrać jedną książkę, czyli przekazywanie dynamicznych parametrów, tak jak w routingu np angulara


# @app.get(
#     "/books/{dynamic_param:str}"
# )  # jeśli przekażemy jako liczbę to fast api zamieni go teraz na string
# async def read_all_books(dynamic_param):
#     return {"dynamic_param": dynamic_param}


# należy pamiętać że kolejność ma znaczenie, tzn jeżeli poniżej mam endpoint kończący się nazwą mybook i pod taką samą nazwą
# przekażę dynamiczny parametr to poniższy endpoint nigdy nie zostanie wykonany, dlatego najpierw pisz statyczne enpointy później
# dynamiczne


# @app.get(
#     "/books/mybook"
# )  # do prawidłowego działania ten endpoint powinen być nad dynamicznym, fast api sprawdza endpointy od góry do dołu (w Express to samo)
# async def read_all_books():
#     return {"book_title": "My favorite book!"}


@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book


# endpoint z query params, przekazywane są jako parametry do naszej funkcji w endpoincie, nie podajemy ich w ścieżce dekoratora


@app.get("/books/")  # tak zapisana ścieżka daje znać fast api że po / bedą query params
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return


# przykład enpointu z dynamicznym parametrem oraz query param
@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if (
            book.get("author").casefold() == book_author.casefold()
            and book.get("category").casefold() == category.casefold()
        ):
            books_to_return.append(book)

    return books_to_return
