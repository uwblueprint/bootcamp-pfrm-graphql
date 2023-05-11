import graphene
from graphql import GraphQLError
from mongoengine.errors import NotUniqueError

from ..graphql.services import services

from .types import Mutation, MutationList, QueryList

class Restaurant(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String(required=True)
    address = graphene.String()
    type = graphene.String()
    budget = graphene.String()
    description = graphene.String()
    rating = graphene.Int()

class RestaurantInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    address = graphene.String(required=True)
    type = graphene.String(required=True)
    budget = graphene.String(required=True)
    description = graphene.String(required=True)
    rating = graphene.Int(required=True)
    
# Queries

# Return object for queries
class RestaurantQueries(QueryList):
    getAllRestaurants = graphene.List(
        Restaurant,
    )
    getRestaurantById = graphene.Field(
        Restaurant, id=graphene.String(required=True)
    )

    def resolve_getAllRestaurants(self, info):
      restaurant_dtos = services[
          "restaurant_service"
      ].get_restaurants()

      return [
          Restaurant(
            id = restaurant_dto["id"],
            name = restaurant_dto["name"],
            address = restaurant_dto["address"],
            type = restaurant_dto["type"],
            budget = restaurant_dto["budget"],
            description = restaurant_dto["description"],
            rating = restaurant_dto["rating"],
          )
          for restaurant_dto in restaurant_dtos
      ]

    def resolve_getRestaurantById(self, info, id):
      restaurant_dto = services[
          "restaurant_service"
      ].get_restaurant(id)
      return Restaurant(
        id = restaurant_dto["id"],
        name = restaurant_dto["name"],
        address = restaurant_dto["address"],
        type = restaurant_dto["type"],
        budget = restaurant_dto["budget"],
        description = restaurant_dto["description"],
        rating = restaurant_dto["rating"],
      )


# Mutations

class CreateRestaurant(Mutation):
    class Arguments:
      restaurant = RestaurantInput(required=True)

    new_restaurant = graphene.Field(Restaurant)

    def mutate(self, info, restaurant):
      restaurant_dto = services[
          "restaurant_service"
      ].create_restaurant(restaurant=restaurant)
      new_restaurant = Restaurant(
        id = restaurant_dto["id"],
        name = restaurant_dto["name"],
        address = restaurant_dto["address"],
        type = restaurant_dto["type"],
        budget = restaurant_dto["budget"],
        description = restaurant_dto["description"],
        rating = restaurant_dto["rating"],
      )

      return CreateRestaurant(new_restaurant=new_restaurant)



class UpdateRestaurant(Mutation):
    class Arguments:
      id = graphene.ID(required=True)
      restaurant = RestaurantInput(required=True)


    updated_restaurant = graphene.Field(Restaurant)

    def mutate(self, info, id, restaurant):
        restaurant_dto = services[
            "restaurant_service"
        ].update_restaurant(id, restaurant)
        updated_restaurant = Restaurant(
          id = restaurant_dto["id"],
          name = restaurant_dto["name"],
          address = restaurant_dto["address"],
          type = restaurant_dto["type"],
          budget = restaurant_dto["budget"],
          description = restaurant_dto["description"],
          rating = restaurant_dto["rating"],
        )

        return UpdateRestaurant(updated_restaurant=updated_restaurant)


class DeleteRestaurant(Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    deleted_restaurant = graphene.Field(Restaurant)

    def mutate(self, info, id):
        restaurant_dto = services[
            "restaurant_service"
        ].delete_restaurant(id)
        deleted_restaurant = Restaurant(
          id = restaurant_dto["id"],
          name = restaurant_dto["name"],
          address = restaurant_dto["address"],
          type = restaurant_dto["type"],
          budget = restaurant_dto["budget"],
          description = restaurant_dto["description"],
          rating = restaurant_dto["rating"],
        )

        return DeleteRestaurant(deleted_restaurant=deleted_restaurant)


class RestaurantMutations(MutationList):
    createRestaurant = CreateRestaurant.Field()
    updateRestaurant = UpdateRestaurant.Field()
    deleteRestaurant = DeleteRestaurant.Field()
