from fastapi import FastAPI

app = FastAPI()


@app.get("/api-endpoint")
async def get_books():  # w fast api async jest dodawany automatycznie, ale można go dodać ręcznie
    return {"message": "Hello, Skolo"}
