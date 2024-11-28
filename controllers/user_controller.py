from flask import render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt

class UserController:
    def __init__(self, db):
        self.db = db
        self.bcrypt = Bcrypt()

    def render_login(self):
        return render_template('login.html')

    def login(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = self.db.users.find_one({"username": username})

            if user and self.bcrypt.check_password_hash(user['password'], password):
                session['user_id'] = str(user['_id'])
                session['username'] = username
                return redirect(url_for('todo_routes.home'))
            else:
                flash("User not found. Please sign up.", "danger")
                return redirect(url_for('user_routes.signup'))

        return render_template('login.html')

    def signup(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            existing_user = self.db.users.find_one({"username": username})
            if existing_user:
                return "Username already exists. Please choose another."

            hashed_password = self.bcrypt.generate_password_hash(
                password).decode('utf-8')
            self.db.users.insert_one(
                {"username": username, "password": hashed_password})

            return redirect(url_for('user_routes.render_login'))

        return render_template('signup.html')

    def logout(self):
        session.pop('user_id', None)
        session.pop('username', None)
        return redirect(url_for('user_routes.render_login'))