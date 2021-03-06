"""
Initialize Flask app

"""
from flask import Flask
import os
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.debug import DebuggedApplication


# App needs to be initialised before any other modules 
# that are dependent on app (e.g views.home)
app = Flask('application')

"""
import all blueprint modules
"""
from views.home import home
from views.landing.landing import landing
# from api.external_api import external_api
from request_handler.handler import handler

if os.getenv('FLASK_CONF') == 'DEV':
	#development settings n
    app.config.from_object('application.settings.Development')
	# Flask-DebugToolbar (only enabled when DEBUG=True)
    toolbar = DebugToolbarExtension(app)
    
    # Google app engine mini profiler
    # https://github.com/kamens/gae_mini_profiler
    app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

    from gae_mini_profiler import profiler, templatetags 
    @app.context_processor
    def inject_profiler():
        return dict(profiler_includes=templatetags.profiler_includes())
    app.wsgi_app = profiler.ProfilerWSGIMiddleware(app.wsgi_app)

elif os.getenv('FLASK_CONF') == 'TEST':
    app.config.from_object('application.settings.Testing')

else:
    app.config.from_object('application.settings.Production')

# Enable jinja2 loop controls extension
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

# Pull in URL dispatch routes - here all blueprints are registered
app.register_blueprint(home)
app.register_blueprint(landing)
# app.register_blueprint(external_api)
app.register_blueprint(handler)