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
