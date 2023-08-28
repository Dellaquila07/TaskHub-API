import webapp2

from views.users import UsersHandler, UserHandler
from views.projects import ProjectsHandler, ProjectHandler


app = webapp2.WSGIApplication([
    webapp2.Route(
        '/projects',
        handler=ProjectsHandler,
        name='projects'
    ),
    webapp2.Route(
        '/project/<project_id>',
        handler=ProjectHandler,
        name='project'
    ),
    webapp2.Route(
        '/users',
        handler=UsersHandler,
        name='users'
    ),
    webapp2.Route(
        '/user/<user_id>',
        handler=UserHandler,
        name='user'
    ),
])
