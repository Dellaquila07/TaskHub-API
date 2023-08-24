import datetime

from models.project import Project
from modules.db_session_manage import DBSessionManage


class ProjectModule(object):
    """Class for ProjectModule"""

    def create(self, params, database):
        """
        Create project
        :params dict params: params to create project
        :params str database: Database
        :return Project
        """
        db_session = DBSessionManage(database).get_db_session()
        try:
            project = Project(database)
            project = self.set_project(project, params)

            db_session.add(project)
            db_session.commit()

            return project

        except:
            db_session.rollback()
            db_session.close()
            raise

    def update(self, project, params, db_session):
        """
        Update project
        :params dict params: params to update project
        :param session db_session: Database session
        """
        if not project:
            raise Exception('ProjectModule: Project is required', 400)

        try:
            project.deadline = params.get('deadline')
            project.description = params.get('description')
            project.designated = params.get('designated')
            project.leader = params.get('leader')
            project.status = params.get('status')
            project.title = params.get('title')

            project.updated_at = datetime.now()

            db_session.add(project)
            db_session.commit()

        except:
            db_session.rollback()
            db_session.close()
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
            db_session.rollback()
            db_session.close()
            raise

    @classmethod
    def search_by_filter_params(cls, params, database):
        """
        Search projects by filter params
        :param dict params: Request params
        :param str database: Database
        :return dict: Search projects response
        """
        db_session = DBSessionManage(database).get_db_session()

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

    @classmethod
    def set_project(cls, project, params):
        """
        Set fields values of Project
        :param project project: Project model
        :param dict params: Project params
        :param session db_session: Database session
        :return Project
        """
        setattr(project, 'deadline', params.get('deadline'))
        setattr(project, 'description', params.get('description'))
        setattr(project, 'designated', params.get('designated'))
        setattr(project, 'leader', params.get('leader'))
        setattr(project, 'status', params.get('status'))
        setattr(project, 'title', params.get('title'))

        return project

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
