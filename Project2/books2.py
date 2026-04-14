from fastapi import FastAPI

app = FastAPI()


class Book:
    def __init__(self, id: int, title: str, author: str, description: str, rating: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


BOOKS = [
    Book(
        1,
        "Dune",
        "Frank Herbert",
        "A noble family becomes embroiled in a war for control over the galaxy's most valuable asset.",
        5,
    ),
    Book(
        2,
        "1984",
        "George Orwell",
        "A dystopian social science fiction novel and cautionary tale about totalitarianism.",
        5,
    ),
    Book(
        3,
        "The Great Gatsby",
        "F. Scott Fitzgerald",
        "The story of the mysteriously wealthy Jay Gatsby and his love for the beautiful Daisy Buchanan.",
        4,
    ),
    Book(
        4,
        "To Kill a Mockingbird",
        "Harper Lee",
        "A novel about the serious issues of rape and racial inequality told through the eyes of a child.",
        5,
    ),
    Book(
        5,
        "The Hobbit",
        "J.R.R. Tolkien",
        "A fantasy novel following the quest of home-loving hobbit Bilbo Baggins to win a share of treasure.",
        5,
    ),
    Book(
        6,
        "Brave New World",
        "Aldous Huxley",
        "A prophetic novel that describes a utopian society based on pleasure and social engineering.",
        4,
    ),
    Book(
        7,
        "The Catcher in the Rye",
        "J.D. Salinger",
        "A story about teenager Holden Caulfield's experiences in New York City after being expelled from prep school.",
        3,
    ),
    Book(
        8,
        "Foundation",
        "Isaac Asimov",
        "A mathematician develops a theory to predict the fall of a galactic empire and save knowledge.",
        5,
    ),
    Book(
        9,
        "Neuromancer",
        "William Gibson",
        "A washed-up computer hacker is hired for one last job that brings him up against a powerful AI.",
        4,
    ),
    Book(
        10,
        "The Witcher: The Last Wish",
        "Andrzej Sapkowski",
        "A collection of short stories introducing Geralt of Rivia, a monster hunter for hire.",
        5,
    ),
    Book(
        11,
        "Pride and Prejudice",
        "Jane Austen",
        "A romantic novel of manners that charts the emotional development of protagonist Elizabeth Bennet.",
        4,
    ),
    Book(
        12,
        "Fahrenheit 451",
        "Ray Bradbury",
        "A novel about a future American society where books are outlawed and 'firemen' burn any that are found.",
        5,
    ),
    Book(
        13,
        "Project Hail Mary",
        "Andy Weir",
        "A lone astronaut must save the earth from disaster using only his scientific wits.",
        5,
    ),
    Book(
        14,
        "The Alchemist",
        "Paulo Coelho",
        "An allegorical novel about a young Andalusian shepherd in his journey to the pyramids of Egypt.",
        4,
    ),
    Book(
        15,
        "The Shining",
        "Stephen King",
        "A family stays in an isolated hotel for the winter where an evil spiritual presence influences the father.",
        4,
    ),
    Book(
        16,
        "Circe",
        "Madeline Miller",
        "A bold retelling of the life of the daughter of Helios, the sun god, who is banished to a deserted island.",
        5,
    ),
    Book(
        17,
        "Sapiens",
        "Yuval Noah Harari",
        "A brief history of humankind, exploring how biology and history have defined us.",
        5,
    ),
    Book(
        18,
        "The Martian",
        "Andy Weir",
        "An astronaut becomes stranded on Mars and must use his ingenuity to survive until rescue.",
        5,
    ),
    Book(
        19,
        "Murder on the Orient Express",
        "Agatha Christie",
        "Famous detective Hercule Poirot investigates a murder on a luxurious train stuck in the snow.",
        4,
    ),
    Book(
        20,
        "American Gods",
        "Neil Gaiman",
        "A story of a war between the Old Gods of mythology and the New Gods of technology and media.",
        4,
    ),
]


@app.get("/books")
async def read_all_books():
    return BOOKS
