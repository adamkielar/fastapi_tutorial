from enum import Enum
from typing import Optional

from fastapi import FastAPI


class ModelName(str, Enum):
    ALEXNET = 'alexnet'
    RESNET = 'resnet'
    LENET = 'lenet'


app = FastAPI()


@app.get("/")
async def root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.ALEXNET:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
