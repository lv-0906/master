from .users import users_bp
from .family import family_bp  


def register_blueprints(app):
    app.register_blueprint(users_bp)
    app.register_blueprint(family_bp)
