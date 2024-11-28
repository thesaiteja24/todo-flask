from flask import Blueprint

def create_todo_routes(todo_controller):
    todo_routes = Blueprint('todo_routes', __name__)

    @todo_routes.route('/home')
    def home():
        return todo_controller.home()

    @todo_routes.route('/createListing.html', methods=['POST', 'GET'])
    def create_listing():
        return todo_controller.create_listing()

    @todo_routes.route('/complete_todo/<todo_id>', methods=['POST'])
    def complete_todo(todo_id):
        return todo_controller.complete_todo(todo_id)

    @todo_routes.route('/view_history')
    def view_history():
        return todo_controller.view_history()

    @todo_routes.route('/delete_todo/<todo_id>', methods=['POST'])
    def delete_todo(todo_id):
        return todo_controller.delete_todo(todo_id)

    @todo_routes.route('/edit_todo/<todo_id>', methods=['GET'])
    def edit_todo_form(todo_id):
        return todo_controller.edit_todo_form(todo_id)

    @todo_routes.route('/update_todo/<todo_id>', methods=['POST'])
    def update_todo(todo_id):
        return todo_controller.update_todo(todo_id)

    @todo_routes.route('/delete_completed_todo/<todo_id>', methods=['POST'])
    def delete_completed_todo(todo_id):
        return todo_controller.delete_completed_todo(todo_id)

    return todo_routes