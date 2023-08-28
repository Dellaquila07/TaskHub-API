import datetime

from models.user import User
from modules.db_session_manage import DBSessionManage


class UserModule(object):
    """Class for UserModule"""

    def create(self, params, database):
        """
        Create user
        :params dict params: params to create user
        :params str database: Database
        :return User
        """
        db_session = DBSessionManage(database).get_db_session()
        try:
            user = User(database)
            user = self.set_user(user, params)

            db_session.add(user)
            db_session.commit()

            return user

        except:
            db_session.rollback()
            db_session.close()
            raise

    def update(self, user, params, db_session):
        """
        Update user
        :params dict params: params to update user
        :param session db_session: Database session
        """
        if not user:
            raise Exception('UserModule: User is required', 400)

        try:
            user.fullname = params.get('fullname')

            user.updated_at = datetime.now()

            db_session.add(user)
            db_session.commit()

        except:
            db_session.rollback()
            db_session.close()
            raise

    def delete(self, user, db_session):
        """
        Delete user
        :params dict user: User to delete
        :param session db_session: Database session
        """
        try:
            db_session.delete(user)
            db_session.flush()
            db_session.commit()

        except:
            db_session.rollback()
            db_session.close()
            raise

    @classmethod
    def search_by_filter_params(cls, params, database):
        """
        Search users by filter params
        :param dict params: Request params
        :param str database: Database
        :return dict: Search users response
        """
        db_session = DBSessionManage(database).get_db_session()

        users, count = User.get_by_filter_params(params, database)

        response = cls.get_default_response()
        response['count'] = count
        response['users'] = cls.users_to_dict(users, db_session)

        db_session.close()

        return response

    @classmethod
    def set_user(cls, user, params):
        """
        Set fields values of User
        :param user user: User model
        :param dict params: User params
        :param session db_session: Database session
        :return User
        """
        setattr(user, 'fullname', params.get('fullname'))

        return user

    @classmethod
    def users_to_dict(cls, users, db_session):
        """
        Return users in dict format
        :param list of user: List with users
        :param session db_session: Database session
        :return list(dict): List with users in dict format
        """
        users_dict = []
        for user in users:
            user_dict = {
                'id': user.id,
                'created_at': user.created_at,
                'fullname': user.fullname,
                'projects_designated': None,
                'projects_leader': None,
                'updated_at': user.updated_at
            }
            cls.set_projects_designated(user.id, user_dict, db_session)
            cls.set_projects_leader(user.id, user_dict, db_session)

            users_dict.append(user_dict)

        return users_dict

    @staticmethod
    def get_default_response():
        """
        Get users default response
        :return dict: Users default response
        """
        return {
            'count': 0,
            'users': []
        }

    @staticmethod
    def set_projects_designated(user_id, user_dict, db_session):
        """
        Set projects in user dict
        :param int user_id: User id
        :param dict user_dict: User dict
        :param session db_session: Database session
        """
        projects_id = []
        projects = User.get_designated_by_project_id(user_id, db_session)

        if projects:
            for project in projects:
                projects_id.append(project.id)

        user_dict['projects_designated'] = projects_id

    @staticmethod
    def set_projects_leader(user_id, user_dict, db_session):
        """
        Set projects in user dict
        :param int user_id: User id
        :param dict user_dict: User dict
        :param session db_session: Database session
        """
        projects_id = []
        projects = User.get_leader_by_project_id(user_id, db_session)

        if projects:
            for project in projects:
                projects_id.append(project.id)

        user_dict['projects_leader'] = projects_id
