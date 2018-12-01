routes = [
    (r'/', 'app.handlers.Profile.Index'),
    (r'/admin/?', 'app.handlers.Admin.Admin'),
    (r'/search/?', 'app.handlers.Search.Search'),
    (r'/profile/?(?P<login>[a-zA-Z0-9\-_]+)/?', 'app.handlers.Profile.Index'),

    (r'/login/?', 'app.handlers.Auth.Signin'),
    (r'/logout/?', 'app.handlers.Auth.Logout'),
    (r'/register/?', 'app.handlers.Auth.Register'),

    (r'/ajax', 'app.handlers.Ajax.Ajax'),

    (r'/create', 'app.handlers.Helpers.CreateUsers'),   # Just for testing
]
