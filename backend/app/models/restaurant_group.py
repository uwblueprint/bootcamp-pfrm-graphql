import mongoengine as mg
from restaurant import Restaurant

class RestaurantGroup(mg.Document):
  name = mg.StringField(required=True)
  description = mg.StringField()
  restaurants = ListField(ReferenceField(Restaurant))

  def to_serializable_dict(self):
    """
    Returns a dict representation of the document that is JSON serializable

    ObjectId must be converted to a string.
    """
    restaurant_dict = self.to_mongo().to_dict()
    id = restaurant_dict.pop("_id", None)
    restaurant_dict["id"] = str(id)
    return restaurant_dict

  meta = {"collection": "restaurants"}
