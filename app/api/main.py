from enum import Enum
from typing import Dict, List, Optional, Set, Union

from fastapi import Body, Cookie, FastAPI, Header, Path, Query, status, File, \
    UploadFile
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: Optional[str] = Field(
        None, title="The description of the item", max_length=300
    )
    price: float = Field(..., gt=0, description="The price must be greater")
    tax: Optional[float] = None
    tags: Set[str] = set()
    image: Optional[List[Image]] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }


class User(BaseModel):
    username: str
    full_name: Optional[str] = None


class ModelName(str, Enum):
    ALEXNET = 'alexnet'
    RESNET = 'resnet'
    LENET = 'lenet'


fake_items_db = [
    {"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}
]


@app.get("/")
async def root():
    return {"Hello": "World"}


@app.get("/items/")
async def read_items(
        skip: int = 0,
        limit: int = 10,
        ads_id: Optional[str] = Cookie(None),
        user_agent: Optional[str] = Header(None)
):
    return fake_items_db[skip: skip + limit], \
           {"ads_id": ads_id}, \
           {"User-Agent": user_agent}


@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.get("/items/{item_id}", response_model=Item,
         response_model_exclude_unset=True)
def read_item(
        item_id: int = Path(..., title="The ID of the item to get", ge=1),
        q: Optional[str] = Query(None, min_length=3, max_length=50, alias="")
):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


@app.put("/items/{item_id}")
async def update_item(
        *,
        item_id: int = Path(..., title="The ID of the item to get", ge=0,
                            le=1000),
        q: Optional[str] = None,
        item: Optional[Item] = None,
        user: User,
        importance: int = Body(..., gt=0),
):
    results = {"item_id": item_id, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.ALEXNET:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
        user_id: int, item_id: str, q: Optional[str] = None,
        short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long desc"}
        )
    return item


@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    return weights


@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}
