from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    store_id = db.Column(db.String, db.ForeignKey('stores.id'), nullable=False)
    store = db.relationship('StoreModel', back_populates='items')
    print("ItemModel initialized")
