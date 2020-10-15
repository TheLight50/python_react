from typing import Optional
from fastapi import FastAPI
from model import Item

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items")
def read_all_items():
    return [ {"item_id": 3, "name": "tablette"}, {"item_id": 4, "name": "HDMI"} ]

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.post("items")
def post_item(item_id: int, q: Optional[str] = None):
    #return {"item_id": item_id, "new": q}
    return item

#@app.put("items/{items_id}")
#def update_item(item_id: int, q: Optional[str] = None):
#    return {"item_id": item_id, "modified": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    #return {"item_name": item.name, "item_id": item_id}
    return item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return True
