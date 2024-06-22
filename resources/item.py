import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from marshmallow import Schema, fields
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import ItemModel
from schemas import ItemSchema,ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200,ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError('Deleting an item is not implemented')


    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema)
    def put(self, item_data,item_id):
        item = ItemModel.query.get(item_id)
        if item:
         item.price = item_data["price"]
         item.name = item_data["name"]
        else:
            item = ItemModel(item_id=item_id, **item_data)
        db.session.add(item)
        db.session.commit()
        return item

@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        items = ItemModel.query.all()
        return items
        '''return items.values()'''
    
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self,item_data):
        #item_data = request.get_json()
        print("Received item data:", item_data)
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Failed to add item")
        return item
        """if "price" not in item_data or "store_id" not in item_data or "name" not in item_data:
            abort(400, message="Bad request. Ensure price, store_id, and name are included in the payload.")
        
        print("Current stores:", stores)
        if item_data["store_id"] not in stores:
            print(f"Store ID {item_data['store_id']} not found in stores.")
            abort(400, message="Bad request. Invalid store_id")"""
        
        """for item in items.values():
            if item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]:
                abort(400, message="Item already exists")
        
        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        print("Item added:", item)
        return item, 201"""
