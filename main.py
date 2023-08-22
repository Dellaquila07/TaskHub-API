import webapp2

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
])
