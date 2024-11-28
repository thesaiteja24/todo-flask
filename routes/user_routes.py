from flask import Blueprint

def create_user_routes(user_controller):
    user_routes = Blueprint('user_routes', __name__)

    @user_routes.route("/")
    def render_login():
        return user_controller.render_login()

    @user_routes.route('/login', methods=['POST', 'GET'])
    def login():
        return user_controller.login()

    @user_routes.route('/signup', methods=['POST', 'GET'])
    def signup():
        return user_controller.signup()

    @user_routes.route('/logout')
    def logout():
        return user_controller.logout()

    return user_routes