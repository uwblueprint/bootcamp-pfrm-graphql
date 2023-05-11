import graphene

from flask import current_app

from .services import services
from ..services.restaurant_service import RestaurantService
from .restaurant import RestaurantMutations, RestaurantQueries


class RootQuery(
    # All queries listed here will be merged.
    RestaurantQueries,
):
    pass


class RootMutation(
    # All mutations listed here will be merged.
    RestaurantMutations,
):
    pass


schema = graphene.Schema(
    query=RootQuery,
    mutation=RootMutation,
)


def init_app(app):
    with app.app_context():
        # Add your services here: services["service_name"] = ...
        services["restaurant_service"] = RestaurantService(logger=current_app.logger)
