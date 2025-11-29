from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Tea(BaseModel):
    id: int
    name: str
    origin: str


teas: List[Tea] = []


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/teas")
def get_teas():
    return teas


@app.post("/teas")
def add_tea(tea: Tea):
    teas.append(tea)
    return tea


@app.put("/teas/{id}")
def update_tea(id: int, tea: Tea):
    for index, tea in enumerate(teas):
        if tea.id == id:
            teas[index] = tea
            return tea
    return {"error": "Tea not found"}


@app.delete("/teas/{id}")
def delete_tea(id: int):
    for index, tea in enumerate(teas):
        if tea.id == id:
            deleted = teas.pop(index)
            return {"deleted": deleted, "message": "Tea deleted"}
    return {"error": "Tea not found"}
