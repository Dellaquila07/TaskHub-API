import datetime

from sqlalchemy import text
from models.project import Project


class ProjectModule(object):
    """Class for ProjectModule"""

    def __init__(self, database, db_session):
        """
        Init project module
        :param str database: Namespace
        :param session db_session: Database session
        """
        self.project = None
        self.database = database
        self.db_session = db_session

    def create(self, params, database):
        """
        Create project
        :params dict params: params to create project
        :params str database: Namespace
        :return Project
        """
        db_session = None # to implement
        try:
            project = Project(database)

            db_session.add(project)
            db_session.commit()

            return project

        except:
            db_session.rollback()
            db_session.close()
            raise

    def update(self, params):
        """
        Update project
        :params dict params: params to update project
        """
        if not self.project:
            raise Exception('ProjectModule: Project is required', 400)

        try:
            self.project.deadline = params.get('deadline')
            self.project.description = params.get('description')
            self.project.designated = params.get('designated')
            self.project.leader = params.get('leader')
            self.project.status = params.get('status')
            self.project.title = params.get('title')

            self.project.updated_at = datetime.now()

            self.db_session.add(self.project)
            self.db_session.commit()

        except:
            self.db_session.rollback()
            self.db_session.close()
            raise
        

    def delete(self, project, db_session):
        """
        Delete project
        :params dict project: Project to delete
        :param session db_session: Database session
        """
        try:
            db_session.delete(project)
            db_session.flush()
            db_session.commit()

        except:
            self.db_session.rollback()
            self.db_session.close()
            raise

    @classmethod
    def search_by_filter_params(cls, params, database):
        """
        Search projects by filter params
        :param dict params: Request params
        :param str database: Database
        :return dict: Search projects response
        """
        db_session = None # to implement

        projects, count = Project.get_by_filter_params(params, database)

        response = cls.get_default_response()
        response['count'] = count
        response['projects'] = cls.projects_to_dict(projects)

        db_session.close()

        return response

    @classmethod
    def projects_to_dict(cls, projects):
        """
        Return invoices in dict format
        :param list of project: List with projects
        :return list(dict): List with projects in dict format
        """
        projects_dict = []
        for project in projects:
            project_dict = {
                'id': project.id,
                'created_at': project.created_at,
                'deadline': project.deadline,
                'description': project.description,
                'designated': project.designated,
                'leader': project.leader,
                'status': project.status,
                'title': project.title,
                'updated_at': project.updated_at
            }
            projects_dict.append(project_dict)

        return projects_dict

    @staticmethod
    def get_default_response():
        """
        Get projects default response
        :return dict: Projects default response
        """
        return {
            'projects': [],
            'count': 0,
        }
