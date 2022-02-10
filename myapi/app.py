from flask import Flask
from flask_cors import CORS

from myapi.common.lib import Lib, MyJSONEncoder
from myapi.extensions import apispec, celery, toolbar, db, mdb, jwt, ma, migrate, logger
from myapi import api, graphql


def create_app(testing=False):
    """Application factory, used to create application"""
    app = Flask("myapi")
    app.config.from_object("myapi.config")

    CORS(app, supports_credentials=True)

    app.json_encoder = MyJSONEncoder
    ma.SQLAlchemyAutoSchema.on_bind_field = Lib.camel_case

    if testing is True:
        app.config["TESTING"] = True

    configure_extensions(app)
    configure_apispec(app)
    register_blueprints(app)
    init_celery(app)

    return app


def configure_extensions(app):
    """configure flask extensions"""
    toolbar.init_app(app)
    db.init_app(app)
    mdb.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    logger.init_app(app)


def configure_apispec(app):
    """Configure APISpec for swagger support"""
    apispec.init_app(app, security=[{"jwt": []}])
    apispec.spec.components.security_scheme(
        "jwt", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    )
    apispec.spec.components.schema(
        "PaginatedResult",
        {
            "properties": {
                "total": {"type": "integer"},
                "pages": {"type": "integer"},
                "next": {"type": "string"},
                "prev": {"type": "string"},
            }
        },
    )


def register_blueprints(app):
    """register all blueprints for application"""
    app.register_blueprint(api.trigger.views.blueprint)
    app.register_blueprint(api.auth.views.blueprint)
    app.register_blueprint(api.endpoint.views.blueprint)
    app.register_blueprint(graphql.views.blueprint)


def init_celery(app=None):
    app = app or create_app()
    celery.conf.update(app.config.get("CELERY", {}))

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
