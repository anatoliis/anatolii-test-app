routes = [
    (r"/", "app.handlers.profile.Index"),
    (r"/admin/?", "app.handlers.admin.Admin"),
    (r"/search/?", "app.handlers.search.Search"),
    (r"/profile/?(?P<login>[a-zA-Z0-9\-_]+)/?", "app.handlers.profile.Index"),
    (r"/login/?", "app.handlers.auth.SignIn"),
    (r"/logout/?", "app.handlers.auth.Logout"),
    (r"/register/?", "app.handlers.auth.Register"),
    (r"/ajax", "app.handlers.ajax.Ajax"),
    (r"/create", "app.handlers.helpers.CreateUsers"),  # Just for testing
]
