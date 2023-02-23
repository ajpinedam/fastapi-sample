
# main.py

import uuid
from datetime import datetime

import fastapi
from pydantic import BaseModel
from fastapi import FastAPI, Query, Path, HTTPException

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Confoo Canada!"}


class Product(BaseModel):
    product_id: int
    name: str
    description: str | None
    tags: list[str] = []
    price: float


products:list[Product] = [
    Product(product_id=100001, name="Keyboard K11", tags=["alice", "2023"], price=200.10),
    Product(product_id=100002, name="Keyboard M23", tags=["65%", "2023"], price=189.00),
    Product(product_id=100015, name="Desktop Mat", tags=["trending", "2022"], price=63.50),
    Product(product_id=100029, name="Mouse Pad", price=63.50),
]


@app.get("/products/", tags=["products"])
async def get_products(
        t: int | None = Query(default=None, alias="take", gt=0)) -> list[Product]:
    if t:
        take = min(len(products), t)
        return products[0:take]
    return products


@app.post("/product/", status_code=fastapi.status.HTTP_201_CREATED, tags=["products"])
async def create_product(product: Product) -> Product:
    if not product.tags:
        product.tags = ["fast", "api"]
    products.append(product)
    return product


@app.get("/product/{product_id}",
         name="Get a Product by Id",
         description="This will find the product using their Id but will return None when not found",
         tags=["products"])
async def get_product(
        product_id: int = Path(title="The Id of the Product to Get")) -> Product:
    result = next((item for item in products if item.product_id == product_id), None)

    if not result:
        raise HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="Product not found")

    return result


@app.delete("/product/{product_id}", tags=["products"])
async def delete_product(product_id: int):
    # find product and delete it
    products[:] = (value for value in products if value.product_id != product_id)


@app.get("/hello/{name}", tags=["utils"])
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/time/", tags=["generic"])
async def get_time(age: int = Query(default=0, description="Enter your age", le=80, gt=18)):
    # We don't need this validation anymore
    if age < 18:
        return None

    return {
        "uuid": uuid.uuid4(),
        "time": datetime.now()
    }
