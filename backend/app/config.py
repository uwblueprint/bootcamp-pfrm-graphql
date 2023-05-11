import os


class Config(object):
    """
    Common configurations
    """

    # put any configurations here that are common across all environments
    # list of available configs: https://flask.palletsprojects.com/en/1.1.x/config/
    MONGODB_URL = os.getenv("MG_DATABASE_URL")


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True

app_config = {
    "development": DevelopmentConfig,
}
