from flask import Flask, request, session
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "super-secret"  # required for sessions

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# ---------------------------
# RESOURCES
# ---------------------------

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")

        if not username:
            return {"error": "Username required"}, 400

        user = User.query.filter_by(username=username).first()
        if not user:
            return {"error": "User not found"}, 404

        session["user_id"] = user.id
        return user.to_dict(), 200


class Logout(Resource):
    def delete(self):
        session.pop("user_id", None)
        return {}, 204


class CheckSession(Resource):
    def get(self):
        user_id = session.get("user_id")
        if not user_id:
            return {}, 401

        user = User.query.get(user_id)
        if not user:
            return {}, 401

        return user.to_dict(), 200


# ---------------------------
# ROUTES
# ---------------------------
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(CheckSession, "/check_session")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
