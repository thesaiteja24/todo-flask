from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
from pytz import timezone
from bson import ObjectId
import calendar

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Class"
app.secret_key = "your_secret_key"  # Required for session management

db = PyMongo(app).db
bcrypt = Bcrypt(app)


@app.route("/")
def renderLogin():
    """
    Render the login page.
    """
    return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    """
    Handle user login.
    - If POST request, authenticate the user.
    - If GET request, render the login page.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.users.find_one({"username": username})

        if user and bcrypt.check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['username'] = username  # Store the username in session
            return redirect(url_for('home'))
        else:
            flash("User not found. Please sign up.", "danger")
            return redirect(url_for('signup'))  # Redirect to signup page

    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    """
    Handle user signup.
    - If POST request, create a new user.
    - If GET request, render the signup page.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = db.users.find_one({"username": username})
        if existing_user:
            return "Username already exists. Please choose another."

        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')
        db.users.insert_one(
            {"username": username, "password": hashed_password})

        return redirect(url_for('renderLogin'))

    return render_template('signup.html')


@app.route('/logout')
def logout():
    """
    Log the user out by clearing the session.
    """
    session.pop('user_id', None)  # Remove the user_id from session
    session.pop('username', None)  # Remove the username from session
    return redirect(url_for('renderLogin'))  # Redirect to the login page


@app.route('/home')
def home():
    """
    Render the home page, displaying todos for today, this week, this month, and completed todos.
    """
    user_id = session.get('user_id')
    ist = timezone('Asia/Kolkata')

    # Date calculations
    today = datetime.now(ist).strftime('%Y-%m-%d')
    start_of_week = (datetime.now(
        ist) - timedelta(days=datetime.now(ist).weekday())).strftime('%Y-%m-%d')
    end_of_week_date = datetime.now(
        ist) + timedelta(days=(6 - datetime.now(ist).weekday()))
    end_of_week = end_of_week_date.strftime('%Y-%m-%d')
    start_of_month = datetime.now(ist).replace(day=1).strftime('%Y-%m-%d')
    year = datetime.now(ist).year
    month = datetime.now(ist).month
    _, last_day = calendar.monthrange(year, month)
    end_of_month = datetime(year, month, last_day).strftime('%Y-%m-%d')

    # Fetch todos
    todos_today = list(db.todo.find({"user_id": user_id, "deadline": today}))
    todos_this_week = list(db.todo.find({
        "$and": [
            {"user_id": user_id},
            {"deadline": {"$gte": start_of_week}},
            {"deadline": {"$lte": end_of_week}},
            {"deadline": {"$ne": today}},
        ]
    }))
    todos_this_month = list(db.todo.find(
        {"user_id": user_id, "deadline": {"$gte": start_of_month, "$lte": end_of_month}}))

    # Fetch completed todos
    completed_todos = list(db.completed.find({"user_id": user_id}))

    return render_template(
        'index.html',
        todos_today=todos_today,
        todos_this_week=todos_this_week,
        todos_this_month=todos_this_month,
        completed_todos=completed_todos,
        username=session.get('username')
    )


@app.route('/createListing.html', methods=['POST', 'GET'])
def createListing():
    """
    Handle the creation of a new todo listing.
    - If POST request, create a new todo.
    - If GET request, render the create listing page.
    """
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        deadline = request.form['deadline']

        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('login'))

        ist = timezone('Asia/Kolkata')
        created_at_ist = datetime.now(ist).strftime('%Y-%m-%d')

        db.todo.insert_one({
            "title": title,
            "description": description,
            "created_at": created_at_ist,
            "deadline": deadline,
            "user_id": user_id
        })

        return redirect(url_for('home'))

    return render_template('createListing.html')


@app.route('/complete_todo/<todo_id>', methods=['POST'])
def complete_todo(todo_id):
    """
    Mark a todo as completed by moving it from the 'todo' collection to the 'completed' collection.
    """
    todo = db.todo.find_one({"_id": ObjectId(todo_id)})

    if todo:
        db.completed.insert_one(todo)
        db.todo.delete_one({"_id": ObjectId(todo_id)})
        return '', 204  # No content response

    return 'Todo not found', 404


@app.route('/view_history')
def view_history():
    """
    Render the history page showing all completed todos.
    """
    user_id = session.get('user_id')
    completed_todos = list(db.completed.find({"user_id": user_id}))

    return render_template('view_history.html', completed_todos=completed_todos)


@app.route('/delete_todo/<todo_id>', methods=['POST'])
def delete_todo(todo_id):
    """
    Delete a todo from the 'todo' collection.
    """
    todo = db.todo.find_one({"_id": ObjectId(todo_id)})

    if todo:
        db.todo.delete_one({"_id": ObjectId(todo_id)})
        return redirect(url_for('home'))

    return 'Todo not found', 404


@app.route('/edit_todo/<todo_id>', methods=['GET'])
def edit_todo_form(todo_id):
    """
    Render the edit form for a specific todo.
    """
    todo = db.todo.find_one({"_id": ObjectId(todo_id)})

    if todo:
        return render_template('edit_todo.html', todo=todo)

    return 'Todo not found', 404


@app.route('/update_todo/<todo_id>', methods=['POST'])
def update_todo(todo_id):
    """
    Update a todo with new data from the form.
    """
    title = request.form['title']
    description = request.form['description']
    deadline = request.form['deadline']

    result = db.todo.update_one(
        {"_id": ObjectId(todo_id)},
        {"$set": {
            "title": title,
            "description": description,
            "deadline": deadline
        }}
    )

    if result.matched_count:
        return redirect(url_for('home'))

    return 'Todo not found', 404


@app.route('/delete_completed_todo/<todo_id>', methods=['POST'])
def delete_completed_todo(todo_id):
    """
    Delete a completed todo from the 'completed' collection.
    """
    todo = db.completed.find_one({"_id": ObjectId(todo_id)})

    if todo:
        db.completed.delete_one({"_id": ObjectId(todo_id)})
        return redirect(url_for('view_history'))

    return 'Todo not found', 404


if __name__ == "__main__":
    app.run(debug=True)



####################################### SQL ###################################################
# from flask import Flask, render_template, request, redirect, url_for, session, flash
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from datetime import datetime, timedelta
# from pytz import timezone
# import calendar

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/Class'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.secret_key = 'your_secret_key'  # Required for session management

# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)

# # Database models
# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(150), unique=True, nullable=False)
#     password = db.Column(db.String(200), nullable=False)

# class Todo(db.Model):
#     __tablename__ = 'todos'
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200), nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     created_at = db.Column(db.String(50), nullable=False)
#     deadline = db.Column(db.String(50), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

# class Completed(db.Model):
#     __tablename__ = 'completed'
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200), nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     created_at = db.Column(db.String(50), nullable=False)
#     deadline = db.Column(db.String(50), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


# @app.route("/")
# def renderLogin():
#     """
#     Render the login page.
#     """
#     return render_template('login.html')


# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     """
#     Handle user login.
#     - If POST request, authenticate the user.
#     - If GET request, render the login page.
#     """
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username).first()

#         if user and bcrypt.check_password_hash(user.password, password):
#             session['user_id'] = user.id
#             session['username'] = username  # Store the username in session
#             return redirect(url_for('home'))
#         else:
#             flash("User not found. Please sign up.", "danger")
#             return redirect(url_for('signup'))  # Redirect to signup page

#     return render_template('login.html')


# @app.route('/signup', methods=['POST', 'GET'])
# def signup():
#     """
#     Handle user signup.
#     - If POST request, create a new user.
#     - If GET request, render the signup page.
#     """
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         existing_user = User.query.filter_by(username=username).first()
#         if existing_user:
#             return "Username already exists. Please choose another."

#         hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
#         new_user = User(username=username, password=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()

#         return redirect(url_for('renderLogin'))

#     return render_template('signup.html')


# @app.route('/logout')
# def logout():
#     """
#     Log the user out by clearing the session.
#     """
#     session.pop('user_id', None)  # Remove the user_id from session
#     session.pop('username', None)  # Remove the username from session
#     return redirect(url_for('renderLogin'))  # Redirect to the login page


# @app.route('/home')
# def home():
#     """
#     Render the home page, displaying todos for today, this week, this month, and completed todos.
#     """
#     user_id = session.get('user_id')
#     ist = timezone('Asia/Kolkata')

#     # Date calculations
#     today = datetime.now(ist).strftime('%Y-%m-%d')
#     start_of_week = (datetime.now(ist) - timedelta(days=datetime.now(ist).weekday())).strftime('%Y-%m-%d')
#     end_of_week_date = datetime.now(ist) + timedelta(days=(6 - datetime.now(ist).weekday()))
#     end_of_week = end_of_week_date.strftime('%Y-%m-%d')
#     start_of_month = datetime.now(ist).replace(day=1).strftime('%Y-%m-%d')
#     year = datetime.now(ist).year
#     month = datetime.now(ist).month
#     _, last_day = calendar.monthrange(year, month)
#     end_of_month = datetime(year, month, last_day).strftime('%Y-%m-%d')

#     # Fetch todos
#     todos_today = Todo.query.filter_by(user_id=user_id, deadline=today).all()
#     todos_this_week = Todo.query.filter(Todo.user_id == user_id, Todo.deadline >= start_of_week, Todo.deadline <= end_of_week, Todo.deadline != today).all()
#     todos_this_month = Todo.query.filter(Todo.user_id == user_id, Todo.deadline >= start_of_month, Todo.deadline <= end_of_month).all()

#     # Fetch completed todos
#     completed_todos = Completed.query.filter_by(user_id=user_id).all()

#     return render_template(
#         'index.html',
#         todos_today=todos_today,
#         todos_this_week=todos_this_week,
#         todos_this_month=todos_this_month,
#         completed_todos=completed_todos,
#         username=session.get('username')
#     )


# @app.route('/createListing.html', methods=['POST', 'GET'])
# def createListing():
#     """
#     Handle the creation of a new todo listing.
#     - If POST request, create a new todo.
#     - If GET request, render the create listing page.
#     """
#     if request.method == 'POST':
#         title = request.form['title']
#         description = request.form['description']
#         deadline = request.form['deadline']

#         user_id = session.get('user_id')
#         if not user_id:
#             return redirect(url_for('login'))

#         ist = timezone('Asia/Kolkata')
#         created_at_ist = datetime.now(ist).strftime('%Y-%m-%d')

#         new_todo = Todo(title=title, description=description, created_at=created_at_ist, deadline=deadline, user_id=user_id)
#         db.session.add(new_todo)
#         db.session.commit()

#         return redirect(url_for('home'))

#     return render_template('createListing.html')


# @app.route('/complete_todo/<todo_id>', methods=['POST'])
# def complete_todo(todo_id):
#     """
#     Mark a todo as completed by moving it from the 'todos' table to the 'completed' table.
#     """
#     todo = Todo.query.get(todo_id)

#     if todo:
#         completed_todo = Completed(title=todo.title, description=todo.description, created_at=todo.created_at, deadline=todo.deadline, user_id=todo.user_id)
#         db.session.add(completed_todo)
#         db.session.delete(todo)
#         db.session.commit()
#         return '', 204  # No content response

#     return 'Todo not found', 404


# @app.route('/view_history')
# def view_history():
#     """
#     Render the history page showing all completed todos.
#     """
#     user_id = session.get('user_id')
#     completed_todos = Completed.query.filter_by(user_id=user_id).all()

#     return render_template('view_history.html', completed_todos=completed_todos)


# @app.route('/delete_todo/<todo_id>', methods=['POST'])
# def delete_todo(todo_id):
#     """
#     Delete a todo from the 'todos' table.
#     """
#     todo = Todo.query.get(todo_id)

#     if todo:
#         db.session.delete(todo)
#         db.session.commit()
#         return redirect(url_for('home'))

#     return 'Todo not found', 404


# @app.route('/edit_todo/<todo_id>', methods=['GET'])
# def edit_todo_form(todo_id):
#     """
#     Render the edit form for a specific todo.
#     """
#     todo = Todo.query.get(todo_id)

#     if todo:
#         return render_template('edit_todo.html', todo=todo)

#     return 'Todo not found', 404


# @app.route('/update_todo/<todo_id>', methods=['POST'])
# def update_todo(todo_id):
#     """
#     Update a todo with new data from the form.
#     """
#     todo = Todo.query.get(todo_id)

#     if todo:
#         todo.title = request.form['title']
#         todo.description = request.form['description']
#         todo.deadline = request.form['deadline']
#         db.session.commit()
#         return redirect(url_for('home'))

#     return 'Todo not found', 404


# @app.route('/delete_completed_todo/<todo_id>', methods=['POST'])
# def delete_completed_todo(todo_id):
#     """
#     Delete a completed todo from the 'completed' table.
#     """
#     todo = Completed.query.get(todo_id)

#     if todo:
#         db.session.delete(todo)
#         db.session.commit()
#         return redirect(url_for('view_history'))

#     return 'Todo not found', 404


# if __name__ == "__main__":
#     app.run(debug=True)
