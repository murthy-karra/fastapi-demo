from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(title="Simple API", description="A simple FastAPI application")

# Data model
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    
# In-memory database
items_db = []

@app.get("/")
def read_root():
    return {"message": "Welcome to the Simple API"}

@app.get("/items", response_model=List[Item])
def read_items():
    return items_db

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    item = next((item for item in items_db if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items", response_model=Item, status_code=201)
def create_item(item: Item):
    # Check if item with the same ID already exists
    if any(existing.id == item.id for existing in items_db):
        raise HTTPException(status_code=400, detail="Item with this ID already exists")
    items_db.append(item)
    return item

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    for i, item in enumerate(items_db):
        if item.id == item_id:
            # Ensure we keep the same ID
            if updated_item.id != item_id:
                raise HTTPException(status_code=400, detail="Cannot change item ID")
            items_db[i] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for i, item in enumerate(items_db):
        if item.id == item_id:
            del items_db[i]
            return {"message": f"Item {item_id} deleted"}
    raise HTTPException(status_code=404, detail="Item not found")

if __name__ == "__main__":
    # Add some example data
    items_db.append(Item(id=1, name="Laptop", description="High-performance laptop", price=1299.99))
    items_db.append(Item(id=2, name="Smartphone", description="Latest model", price=799.99))
    
    # Run the application
    uvicorn.run(app, host="0.0.0.0", port=8000)
