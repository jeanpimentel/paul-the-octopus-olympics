import os


class Config(object):
    DEBUG: bool = False
    TESTING: bool = False

    JSON_SORT_KEYS: bool = False

    API_TITLE: str = "Paul the Octopus - Olympics"
    API_VERSION: str = "1.0.0"

    OPENAPI_VERSION: str = "3.0.2"
    OPENAPI_URL_PREFIX: str = "/doc"

    OPENAPI_SWAGGER_UI_PATH: str = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.51.1/"

    @property
    def MY_SECRET(self) -> str:
        return os.environ.get("MY_SECRET")


class LocalConfig(Config):
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass


def load_configs(app):
    environments = {
        "local": LocalConfig,
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }

    if "ENV" not in app.config:
        raise ValueError("No ENV set for application")

    if app.config.get("ENV") not in environments:
        raise ValueError("Invalid ENV set for application")

    app.config.from_object(environments.get(app.config.get("ENV"))())

    return app
