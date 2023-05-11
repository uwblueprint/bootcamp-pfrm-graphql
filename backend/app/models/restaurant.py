import mongoengine as mg

RESTAURANT_BUDGET_LOW = "LOW"
RESTAURANT_BUDGET_MEDIUM = "MEDIUM"
RESTAURANT_BUDGET_HIGH = "HIGH"
RESTAURANT_BUDGETS = [
  RESTAURANT_BUDGET_LOW,
  RESTAURANT_BUDGET_MEDIUM,
  RESTAURANT_BUDGET_HIGH,
]

class Restaurant(mg.Document):
  name = mg.StringField(required=True)
  address = mg.StringField()
  type = mg.StringField()
  budget = mg.StringField(choices=RESTAURANT_BUDGETS)
  description = mg.StringField()
  rating = mg.IntField(min=1, max=5)

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
