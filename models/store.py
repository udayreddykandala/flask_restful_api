from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id= db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(80),unique=True,nullable=False)
    items = db.relationship('ItemModel',back_populates="stores",lazy='dynamic')
    def __init__(self,name):
        self.name = name
        def json(self):
            return {'name':self.name,'items':[item.json() for item in self.items.all()
                                              ]}
        