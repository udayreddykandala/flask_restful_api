from flask import Flask,request,jsonify
import logging
from db import stores,items
from flask_smorest import abort
import uuid

app= Flask(__name__)



@app.get("/store")
def get_stores():
    return { "stores" : list(stores.values())}


@app.post("/store")
def create_store():
    store_data = request.get_json()
    print("Received store data:", store_data)
    
    if store_data is None:
        abort(400, "Bad request. JSON body is missing or malformed.")
    
    if "name" not in store_data:
        abort(400, "Bad request. Store name is required.")
    
    print("Current stores before addition:", stores)
    
    for store in stores.values():
        print("Checking store:", store)
        if isinstance(store, dict) and store_data["name"] == store["name"]:
            abort(400, "Store already exists.")
    
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    print("Store added:", store)
    print("Current stores after addition:", stores)
    return store, 201

@app.post("/item")
def create_item():
    item_data = request.get_json()
    print("Received item data:", item_data)
    
    if (
        "store_id" not in item_data or
        "name" not in item_data or
        "price" not in item_data
    ):
        abort(400, "Bad request. Ensure 'price', 'store_id' and 'name' are included.")
    
    print("Current stores:", stores)
    if item_data["store_id"] not in stores:
        abort(404, "Store not found")
    
    for item in items.values():
        if (item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, "Item already exists")
    
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    print("Item added:", item)
    return item, 201


@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
         return stores[store_id]
    except KeyError:
         abort(404,message = "store not found")



@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404,message = "item not found")

@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "item deleted"}
    except KeyError:
        abort(404,message = "item not found")

@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "store deleted"}
    except KeyError:
        abort(404,message = "store not found")

@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    print("Item data to be updates is :", item_data)
    if "price" not in item_data or "name" not in item_data:
        abort(400, "Bad request. Ensure 'price' and 'name' are included.")
    print("Current items:", items)
    try:
        item = items[item_id]
        # Update the item with the new data
        item.update(item_data)
        items[item_id] = item
        print("Updated item:", item)
        return item
    except KeyError:
        abort(404, "Item not found")


@app.get("/item")
def get_all_items():
    return { "items" : list(items.values()) }
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)