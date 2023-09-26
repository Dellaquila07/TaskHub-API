from models.project import ProjectComments


class ProjectCommentsModule(object):
    """Class for ProjectCommentsModules"""

    def __init__(self, db_session, project):
        """
        Project comments
        :param Session db_session: Database session
        :param Project project: Project
        """
        self.db_session = db_session
        self.project = project
        self._locale = 'pt-BR'

    def create(self, description, user_id):
        """
        Create a new project comment
        :param str description: Description
        :param int user_id: User id
        """
        comment = ProjectComments()
        comment.description = description
        comment.project_id = self.project.id
        comment.reporter = user_id

        self.db_session.add(comment)
