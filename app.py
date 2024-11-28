from flask import Flask
from flask_pymongo import PyMongo
from controllers.user_controller import UserController
from controllers.todo_controller import TodoController
from routes.user_routes import create_user_routes
from routes.todo_routes import create_todo_routes

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Class"
app.secret_key = "your_secret_key"

# Initialize MongoDB
mongo = PyMongo(app)
db = mongo.db

# Initialize controllers
user_controller = UserController(db)
todo_controller = TodoController(db)

# Register blueprints
app.register_blueprint(create_user_routes(user_controller))
app.register_blueprint(create_todo_routes(todo_controller))

if __name__ == "__main__":
    app.run(debug=True)