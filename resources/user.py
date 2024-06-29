from flask.views import MethodView
from flask_smorest import Blueprint,abort
from passlib.hash import pbkdf2_sha256

from db import db
from models import UserModel
from schemas import UserSchema,UserRegisterSchema

blp = Blueprint("Users", "users", description = "operations on user")
@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(200,UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(400, message = "A user with that username already exists.")

        user = UserModel(**user_data)
        user.password = pbkdf2_sha256.hash(user_data["password"])
        db.session.add(user)
        db.session.commit()
        return {"message" : "user created successfully"}, 201
    
@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200,UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    def delete(self,user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message" : "user deleted"}, 200
    
    
        