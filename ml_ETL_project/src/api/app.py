from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    value: float

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/predict")
def predict(item: Item):
    # Fake prediction for testing
    return {"result": item.value * 2}
