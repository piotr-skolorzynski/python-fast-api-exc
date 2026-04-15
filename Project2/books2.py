from fastapi import FastAPI
from pydantic import (
    BaseModel,
    Field,
)  # pydantic - jest biblioteką pythona do modelowania danych, parsowania i ma efektywne metody ogarniania błędów
from typing import Optional

app = FastAPI()


# składnia klasy zgodna z pydantic
class Book(BaseModel):
    id: int
    title: str
    author: str
    description: str
    rating: int


# obiekt określający request przychodzący z frontu, walidacja pól, odbywa się zanim wogóle dojdzie do transformacji requestu do book
class BookRequest(BaseModel):
    # id: Optional[int] = (
    #     None  # deklarowanie opcjonalnego pola, nusi być od wersji 2 zainicjowane None co oznacza że może być int albo None
    # )
    # można ogarnąć to poprze pydantic i zrobić bardziej opisowe w swaggerze, default musi być
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_lenght=100)
    rating: int = Field(gt=0, lt=6)  # gt - grater than, lt - less than (gives 0 to 5)

    # jest możliwość bardziej opisowego przedstawienia modelu w swagger:
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "Krzysztof Jarzyna",
                "description": "It is another great book",
                "rating": 5,
            }
        }
    }


# przerobione obiekty
BOOKS = [
    Book(
        id=1,
        title="Dune",
        author="Frank Herbert",
        description="A noble family becomes embroiled in a war for control over the galaxy's most valuable asset.",
        rating=5,
    ),
    Book(
        id=2,
        title="1984",
        author="George Orwell",
        description="A dystopian social science fiction novel and cautionary tale about totalitarianism.",
        rating=5,
    ),
    Book(
        id=3,
        title="The Great Gatsby",
        author="F. Scott Fitzgerald",
        description="The story of the mysteriously wealthy Jay Gatsby and his love for the beautiful Daisy Buchanan.",
        rating=4,
    ),
    Book(
        id=4,
        title="To Kill a Mockingbird",
        author="Harper Lee",
        description="A novel about the serious issues of rape and racial inequality told through the eyes of a child.",
        rating=5,
    ),
    Book(
        id=5,
        title="The Hobbit",
        author="J.R.R. Tolkien",
        description="A fantasy novel following the quest of home-loving hobbit Bilbo Baggins to win a share of treasure.",
        rating=5,
    ),
    Book(
        id=6,
        title="Brave New World",
        author="Aldous Huxley",
        description="A prophetic novel that describes a utopian society based on pleasure and social engineering.",
        rating=4,
    ),
    Book(
        id=7,
        title="The Catcher in the Rye",
        author="J.D. Salinger",
        description="A story about teenager Holden Caulfield's experiences in New York City after being expelled from prep school.",
        rating=3,
    ),
    Book(
        id=8,
        title="Foundation",
        author="Isaac Asimov",
        description="A mathematician develops a theory to predict the fall of a galactic empire and save knowledge.",
        rating=5,
    ),
    Book(
        id=9,
        title="Neuromancer",
        author="William Gibson",
        description="A washed-up computer hacker is hired for one last job that brings him up against a powerful AI.",
        rating=4,
    ),
    Book(
        id=10,
        title="The Witcher: The Last Wish",
        author="Andrzej Sapkowski",
        description="A collection of short stories introducing Geralt of Rivia, a monster hunter for hire.",
        rating=5,
    ),
    Book(
        id=11,
        title="Pride and Prejudice",
        author="Jane Austen",
        description="A romantic novel of manners that charts the emotional development of protagonist Elizabeth Bennet.",
        rating=4,
    ),
    Book(
        id=12,
        title="Fahrenheit 451",
        author="Ray Bradbury",
        description="A novel about a future American society where books are outlawed and 'firemen' burn any that are found.",
        rating=5,
    ),
    Book(
        id=13,
        title="Project Hail Mary",
        author="Andy Weir",
        description="A lone astronaut must save the earth from disaster using only his scientific wits.",
        rating=5,
    ),
    Book(
        id=14,
        title="The Alchemist",
        author="Paulo Coelho",
        description="An allegorical novel about a young Andalusian shepherd in his journey to the pyramids of Egypt.",
        rating=4,
    ),
    Book(
        id=15,
        title="The Shining",
        author="Stephen King",
        description="A family stays in an isolated hotel for the winter where an evil spiritual presence influences the father.",
        rating=4,
    ),
    Book(
        id=16,
        title="Circe",
        author="Madeline Miller",
        description="A bold retelling of the life of the daughter of Helios, the sun god, who is banished to a deserted island.",
        rating=5,
    ),
    Book(
        id=17,
        title="Sapiens",
        author="Yuval Noah Harari",
        description="A brief history of humankind, exploring how biology and history have defined us.",
        rating=5,
    ),
    Book(
        id=18,
        title="The Martian",
        author="Andy Weir",
        description="An astronaut becomes stranded on Mars and must use his ingenuity to survive until rescue.",
        rating=5,
    ),
    Book(
        id=19,
        title="Murder on the Orient Express",
        author="Agatha Christie",
        description="Famous detective Hercule Poirot investigates a murder on a luxurious train stuck in the snow.",
        rating=4,
    ),
    Book(
        id=20,
        title="American Gods",
        author="Neil Gaiman",
        description="A story of a war between the Old Gods of mythology and the New Gods of technology and media.",
        rating=4,
    ),
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}")
async def read_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book


@app.get("/books/")
async def read_book_by_rating(book_rating: int):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)

    return books_to_return


# enpoint z walidacją
@app.post("/create-book")
async def create_book(
    book_request: BookRequest,  # jak podamy taki model jaki chcemy żeby został przesłany to automatycznie zostanie również wyświetlony w swaggerze
):  # Body jest opcjonalne, bez niego sobie poradzi
    new_book = Book(
        **book_request.model_dump()
    )  # przekaże do konstruktora rozłożony na klucz wartość obiekt book_request
    BOOKS.append(find_book_id(new_book))


# funkcja pomocnicza do generowania id
def find_book_id(book: Book):
    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id + 1
    # else:
    #     book.id = 1

    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1

    return book
