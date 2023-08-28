import json

from urllib.request import BaseHandler

from models.user import User
from modules.user import UserModule
from modules.db_session_manage import DBSessionManage


class UsersHandler(BaseHandler):
    """Class for UsersHandler"""

    def get(self):
        """Get users"""
        try:
            database = None # to implement
            params = self.request.GET
            response = UserModule.search_by_filter_params(params, database)

            self.response_send(response)

        except Exception as error:
            self.response_error(error)

    def post(self):
        """Create user"""
        try:
            database = None # to implement]
            params = self.request.GET
            user = UserModule.create(params, database)

            self.response_send({
                'id': user.id,
                'name': user.fullname
            })

        except Exception as error:
            self.response_error(error)


class UserHandler(BaseHandler):
    """Class for UserHandler"""

    def get(self, user_id):
        """Get user"""
        try:
            database = None # to implement
            db_session = DBSessionManage(database).get_db_session()

            user = User.get_by_id(user_id, db_session)
            user_dict = user.to_dict()

            db_session.close()

            self.response_send(user_dict)

        except Exception as error:
            self.response_error(error)

    def put(self, user_id):
        """Update user"""
        try:
            database = None # to implement
            db_session = DBSessionManage(database).get_db_session()
            params = json.loads(self.request.body)

            user = User.get_by_id(user_id, db_session)

            UserModule.update(user, params, db_session)

            db_session.close()

            self.response_send({
                'user_id': user.id
            })

        except Exception as error:
            self.response_error(error)

    def delete(self, user_id):
        """Delete user"""
        try:
            database = None # to implement
            db_session = DBSessionManage(database).get_db_session()

            user = User.get_by_id(user_id, db_session)
            if not user:
                raise Exception('User not found', 404)

            UserModule.delete(user, db_session)

            self.response_send(status_code=204)

        except Exception as error:
            self.response_error(error)
