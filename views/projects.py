import json

from urllib.request import BaseHandler
from models.project import Project
from modules.project import ProjectModule


class ProjectsHandler(BaseHandler):
    """Class for ProjectsHandler"""

    def get(self):
        """Get projects"""
        try:
            database = None # to implement
            params = self.request.GET
            response = ProjectModule.search_by_filter_params(params, database)

            self.response_send(response)

        except Exception as error:
            self.response_error(error)

    def post(self):
        """Create project"""
        try:
            database = None # to implement]
            params = self.request.GET
            project = ProjectModule.create(params, database)

            self.response_send({
                'id': project.id,
                'name': project.name
            })

        except Exception as error:
            self.response_error(error)


class ProjectHandler(BaseHandler):
    """Class for ProjectHandlerProjectHandler"""

    def get(self, project_id):
        """Get project"""
        try:
            database = None # to implement
            db_session = None # to implement

            project = Project.get_by_id(project_id, db_session)
            project_dict = project.to_dict()

            db_session.close()

            self.response_send(project_dict)

        except Exception as error:
            self.response_error(error)

    def post(self, project_id):
        """Update project"""
        try:
            database = None # to implement
            db_session = None # to implement
            params = json.loads(self.request.body)

            project = Project.get_by_id(project_id, db_session)

            project_module = ProjectModule(database, db_session)
            project_module.project = project
            project_module.update(params)

            db_session.close()

            self.response_send({
                'project_id': project.id
            })

        except Exception as error:
            self.response_error(error)

    def delete(self, project_id):
        """Delete project"""
        try:
            database = None # to implement
            db_session = None # to implement

            project = Project.get_by_id(project_id, db_session)
            if not project:
                raise Exception('Project not found', 404)

            ProjectModule.delete(project, db_session)

            self.response_send(status_code=204)

        except Exception as error:
            self.response_error(error)
