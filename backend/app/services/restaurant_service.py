from ..models.restaurant import Restaurant
from ..resources.restaurant_dto import RestaurantDTO


class RestaurantService():
    """
    RestaurantService implementation with Restaurant management methods
    """

    def __init__(self, logger):
        """
        Create an instance of RestaurantService

        :param logger: application's logger instance
        :type logger: logger
        """
        self.logger = logger

    def get_restaurants(self):
      
      # Extract all the restaurants from the restaurants object document and return them
      # as an array of dictionaries
      
      restaurant_dtos = []
      for restaurant in Restaurant.objects:
          restaurant_dict = restaurant.to_serializable_dict()

          try:
            restaurant_dtos.append(RestaurantDTO(restaurant_dict).restaurant)
          except Exception as e:
            reason = getattr(e, "message", None)
            self.logger.error(
                "Failed to get Restaurants. Reason = {reason}".format(
                    reason=(reason if reason else str(e))
                )
            )
            raise e

      return restaurant_dtos


    def get_restaurant(self, id):
      
      # get queries by the primary key, which is id for the Restaurant table

      try:
        restaurant = Restaurant.objects(id=id).first()

        if not restaurant:
            error_message = f"restaurant_id {id} not found"
            self.logger.error(error_message)
            raise Exception(error_message)

        restaurant_dict = restaurant.to_serializable_dict()
        return RestaurantDTO(restaurant_dict).restaurant
      except Exception as e:
        reason = getattr(e, "message", None)
        self.logger.error(
            "Failed to get user. Reason = {reason}".format(
                reason=(reason if reason else str(e))
            )
        )
        raise e

    def create_restaurant(self, restaurant):
      
      new_restaurant = None

      try:
        new_restaurant = Restaurant(
          name = restaurant.name,
          address = restaurant.address,
          type = restaurant.type,
          budget = restaurant.budget,
          description = restaurant.description,
          rating = restaurant.rating,
        ).save()
      except Exception as e:
        reason = getattr(e, "message", None)
        self.logger.error(
            "Failed to get user. Reason = {reason}".format(
                reason=(reason if reason else str(e))
            )
        )
        raise e
      
      return RestaurantDTO(new_restaurant.to_serializable_dict()).restaurant


    def update_restaurant(self, id, restaurant):

      old_restaurant = None

      try:
        old_restaurant = Restaurant.objects(id=id).modify(
          new=False,
          name = restaurant.name,
          address = restaurant.address,
          type = restaurant.type,
          budget = restaurant.budget,
          description = restaurant.description,
          rating = restaurant.rating,
        )

        if not old_restaurant:
          raise Exception("restaurant_id {id} not found".format(id=id))
        
      except Exception as e:
        reason = getattr(e, "message", None)
        self.logger.error(
            "Failed to get restaurant. Reason = {reason}".format(
                reason=(reason if reason else str(e))
            )
        )
        raise e
      
      return RestaurantDTO(old_restaurant.to_serializable_dict()).restaurant

    def delete_restaurant(self, id):
       
      deleted_restaurant = None

      try:
            deleted_restaurant = Restaurant.objects(id=id).modify(
                remove=True, new=False
            )

            if not deleted_restaurant:
                raise Exception(
                    "Restaurant ID {id} not found".format(
                        id=id
                    )
                ) 
      except Exception as e:
            reason = getattr(e, "message", None)
            self.logger.error(
                "Failed to delete user. Reason = {reason}".format(
                    reason=(reason if reason else str(e))
                )
            )
            raise e
       
      return RestaurantDTO(deleted_restaurant.to_serializable_dict()).restaurant
    