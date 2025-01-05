from fastapi import FastAPI

import api

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "FastAPI"}


@app.get("/api/accidents")
def read_accidents(start: int, size: int):
    return api.read_accidents(start, size)


@app.get("/api/suggestions/{airline}")
def read_airline_suggestions(airline: str):
    return api.read_airline_suggestions(airline)


@app.get("/api/information/{airline}")
def read_airline_info(airline: str):
    return api.read_airline_info(airline)
