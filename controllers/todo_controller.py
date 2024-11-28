from flask import render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
from pytz import timezone
from bson import ObjectId
import calendar

class TodoController:
    def __init__(self, db):
        self.db = db

    def home(self):
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
        todos_today = list(self.db.todo.find({"user_id": user_id, "deadline": today}))
        todos_this_week = list(self.db.todo.find({
            "$and": [
                {"user_id": user_id},
                {"deadline": {"$gte": start_of_week}},
                {"deadline": {"$lte": end_of_week}},
                {"deadline": {"$ne": today}},
            ]
        }))
        todos_this_month = list(self.db.todo.find(
            {"user_id": user_id, "deadline": {"$gte": start_of_month, "$lte": end_of_month}}))

        completed_todos = list(self.db.completed.find({"user_id": user_id}))

        return render_template(
            'index.html',
            todos_today=todos_today,
            todos_this_week=todos_this_week,
            todos_this_month=todos_this_month,
            completed_todos=completed_todos,
            username=session.get('username')
        )

    def create_listing(self):
        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']
            deadline = request.form['deadline']

            user_id = session.get('user_id')
            if not user_id:
                return redirect(url_for('user_routes.login'))

            ist = timezone('Asia/Kolkata')
            created_at_ist = datetime.now(ist).strftime('%Y-%m-%d')

            self.db.todo.insert_one({
                "title": title,
                "description": description,
                "created_at": created_at_ist,
                "deadline": deadline,
                "user_id": user_id
            })

            return redirect(url_for('todo_routes.home'))

        return render_template('createListing.html')

    def complete_todo(self, todo_id):
        todo = self.db.todo.find_one({"_id": ObjectId(todo_id)})

        if todo:
            self.db.completed.insert_one(todo)
            self.db.todo.delete_one({"_id": ObjectId(todo_id)})
            return '', 204

        return 'Todo not found', 404

    def view_history(self):
        user_id = session.get('user_id')
        completed_todos = list(self.db.completed.find({"user_id": user_id}))
        return render_template('view_history.html', completed_todos=completed_todos)

    def delete_todo(self, todo_id):
        todo = self.db.todo.find_one({"_id": ObjectId(todo_id)})

        if todo:
            self.db.todo.delete_one({"_id": ObjectId(todo_id)})
            return redirect(url_for('todo_routes.home'))

        return 'Todo not found', 404

    def edit_todo_form(self, todo_id):
        todo = self.db.todo.find_one({"_id": ObjectId(todo_id)})

        if todo:
            return render_template('edit_todo.html', todo=todo)

        return 'Todo not found', 404

    def update_todo(self, todo_id):
        title = request.form['title']
        description = request.form['description']
        deadline = request.form['deadline']

        result = self.db.todo.update_one(
            {"_id": ObjectId(todo_id)},
            {"$set": {
                "title": title,
                "description": description,
                "deadline": deadline
            }}
        )

        if result.matched_count:
            return redirect(url_for('todo_routes.home'))

        return 'Todo not found', 404

    def delete_completed_todo(self, todo_id):
        todo = self.db.completed.find_one({"_id": ObjectId(todo_id)})

        if todo:
            self.db.completed.delete_one({"_id": ObjectId(todo_id)})
            return redirect(url_for('todo_routes.view_history'))

        return 'Todo not found', 404