# Flask Todo App

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.3-lightgrey.svg)

A **Flask-based Todo App** that allows users to manage tasks with a focus on modularity, efficiency, and user-friendly design. This app supports user authentication, task categorization, and task management, making it a great project to showcase Flask and MongoDB integration.

---

## 🚀 Features

- **User Authentication**: Sign up, log in, and log out functionality with password hashing using `bcrypt`.
- **Task Management**: Create, view, edit, delete, and mark tasks as complete.
- **Dynamic Deadlines**:
  - Tasks due **today**.
  - Tasks due **this week** (excluding today).
  - Tasks due **this month**.
- **History View**: View a list of all completed tasks.
- **Modular Architecture**: Separation of concerns with `controllers` and `routes` for better maintainability.
- **Responsive Design**: Comes with templates ready for adaptation.

---

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Database**: MongoDB
- **Frontend**: HTML, CSS, Jinja2
- **Libraries**:
  - `Flask-Bcrypt` for password hashing.
  - `Flask-PyMongo` for MongoDB integration.
  - `Pytz` for timezone handling.

---

## 📂 Project Structure

```plaintext
project/
├── app.py                # Main application entry point
├── controllers/          # Contains controller logic
│   ├── user_controller.py
│   └── todo_controller.py
├── routes/               # Contains route definitions
│   ├── user_routes.py
│   └── todo_routes.py
├── templates/            # HTML templates for the frontend
│   ├── login.html
│   ├── signup.html
│   ├── index.html
│   └── createListing.html
└── requirements.txt      # Python dependencies
```
Here’s the properly formatted markdown for the provided content:


# Flask Todo App

---

## 🔧 Installation

Follow these steps to set up the project locally:

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/flask-todo-app.git
cd flask-todo-app
```

### 2. Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up MongoDB
1. Ensure MongoDB is installed and running locally.
2. Create a database named `todo-list-flask`.
3. The application will automatically create collections (`users`, `todo`, `completed`) during runtime.

### 5. Run the Application
```bash
python app.py
```

Access the app at: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 📝 Usage

### User Management
- **Sign Up**: Create a new account.
- **Log In**: Log in with existing credentials.

### Task Management
- **Add Task**: Use the "Create Listing" form to add new tasks.
- **View Tasks**: View tasks organized by deadlines (today, this week, this month).
- **Complete Task**: Mark tasks as completed.
- **Edit/Delete Tasks**: Modify or remove tasks as needed.
- **View History**: Access completed tasks.

---

## 🛡️ Security Features

- Passwords are securely hashed using `Flask-Bcrypt`.
- User sessions are managed securely with Flask's session mechanism.
- Sensitive configurations (e.g., `SECRET_KEY`) can be moved to environment variables for production.

---

## 🤝 Contributing

Contributions are welcome! Follow these steps to contribute:

1. Fork this repository.
2. Create a new branch for your feature/bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push them:
   ```bash
   git push origin feature-name
   ```
4. Create a Pull Request.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 📬 Contact

If you have any questions, feel free to reach out:

- **Name**: Sai Teja
- **GitHub**: [thesaiteja24](https://github.com/thesaiteja24)  

---

### 🙌 Acknowledgments

- [Flask Documentation](https://flask.palletsprojects.com/)
- [MongoDB Documentation](https://www.mongodb.com/docs/)
- [Bootstrap](https://getbootstrap.com/) for frontend inspiration
