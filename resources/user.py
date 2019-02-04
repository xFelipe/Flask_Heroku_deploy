from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="this field cant be left blank.")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="this field cant be left blank.")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': "The user '{}' already exists".format(data['username'])}, 400
        else:
            user = UserModel(**data)
            user.save_to_db()
            return {'message': 'user {} was successfully created'.format(data['username'])}
