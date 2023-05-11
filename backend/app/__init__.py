from flask import Flask
from flask.cli import ScriptInfo
from flask_cors import CORS
from graphql_server.flask import GraphQLView
from logging.config import dictConfig

from .config import app_config
from .graphql import schema as graphql_schema


def create_app(config_name):
    # configure Flask logger
    dictConfig(
        {
            "version": 1,
            "handlers": {
                "wsgi": {
                    "class": "logging.FileHandler",
                    "level": "ERROR",
                    "filename": "error.log",
                    "formatter": "default",
                }
            },
            "formatters": {
                "default": {
                    "format": "%(asctime)s-%(levelname)s-%(name)s::%(module)s,%(lineno)s: %(message)s"  # noqa
                },
            },
            "root": {"level": "ERROR", "handlers": ["wsgi"]},
            "loggers": {"app.graphql.error_handling": {"level": "INFO"}},
        }
    )

    app = Flask(__name__, template_folder="templates", static_folder="static")

    app.config.from_object(app_config[config_name])

    app.add_url_rule(
        "/graphql",
        view_func=GraphQLView.as_view(
            "graphql",
            schema=graphql_schema,
            graphiql=True,
        ),
    )

    app.config["CORS_ORIGINS"] = [
        "http://localhost:3000",
    ]
    app.config["CORS_SUPPORTS_CREDENTIALS"] = True
    CORS(app)

    from . import models, graphql

    models.init_app(app)
    graphql.init_app(app)

    return app
