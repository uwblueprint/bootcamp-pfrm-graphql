
class RestaurantDTO:
    def __init__(self, restaurant):
        self.restaurant = restaurant

        error_list = self.validate()
        if len(error_list) > 0:
            error_message = "\n".join(error_list)
            raise Exception(error_message)

    def validate(self):
      error_list = []

      if not isinstance(self.restaurant, dict):
          error_list.append("The restaurant information supplied is not a dict.")
          return error_list
      
      restaurant_fields = ["id", "name", "address", "type", "budget", "description", "rating"]
      for field in restaurant_fields:
        if field not in self.restaurant:
            error_list.append(
                f'The {self.restaurant} supplied does not have field "{field}".'
            )
        if type(self.restaurant[field]) is not str:
            error_list.append(f'The field "{field}" in {self.restaurant} is not a string.')
        if field == "name":
            if self.restaurant[field] == "":
                error_list.append(
                    f'The field "{field}" in {self.restaurant} must not be an empty string.'
                )
        if field == "budget":
            budget_values = {'LOW', 'MEDIUM', 'HIGH'}
            if self.restaurant[field].upper() not in budget_values:
                error_list.append(
                    "Invalid budget value, it must be LOW, MEDIUM, or HIGH"
                )
        
        if field == "rating":
            if int(self.restaurant[field]) < 1 or int(self.restaurant[field]) > 5:
                error_list.append(
                    "Invalid rating value, it must be an integer between 1 and 5 inclusive"
                )
        return error_list