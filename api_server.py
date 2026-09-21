from fastapi import FastAPI

app = FastAPI()


items = [
    {"id": 1, "name": "test-item-1", "price": 1000},
    {"id": 2, "name": "test-item-2", "price": 2000},
    {"id": 3, "name": "test-item-3", "price": 3000},
]


@app.get("/api/items")
def get_items():
    return items


@app.get("/api/items/{item_id}")
def get_item_detail(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item

    return {"message": "Item not found"}


@app.post("/api/items", status_code=201)
def create_item(item: dict):
    new_item = {
        "id": len(items) + 1,
        "name": item.get("name"),
        "price": item.get("price"),
    }

    items.append(new_item)

    return new_item

#   http://127.0.0.1:8000/api/items
#   http://127.0.0.1:8000/docs