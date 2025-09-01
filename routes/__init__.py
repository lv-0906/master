from .users import users_bp
from .family import family_bp  
from .upload import upload_bp
from .orders import orders_bp

def register_blueprints(app):
    app.register_blueprint(users_bp)
    app.register_blueprint(family_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(orders_bp)
