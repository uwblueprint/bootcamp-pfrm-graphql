from mongoengine import connect
import pymongo
from .restaurant_seed_data import restaurant_seed_data

# set erase_db_and_sync = True if you want to seed the database or if you need to change the schema
# be careful since it will drop all existing tables!
#
# typically we would use migrations to modify the DB schema, especially for production apps
# migrations are safer and offer more fine-grained controls. However, for simplicity, we won't use migrations for bootcamp
erase_db_and_sync = False


def init_app(app):
    app.app_context().push()
    # connect to MongoDB
    mongo_client = (
      pymongo.MongoClient
    )

    # instantiate a MongoDB instance
    if "MONGODB_URL" in app.config:
        connect(host=app.config["MONGODB_URL"], mongo_client_class=mongo_client)

    # look at restaurant.py for the model (and table) definition
    from .restaurant import Restaurant

    if erase_db_and_sync:
      # drop all documents
      Restaurant.drop_collection()

      # add seed data
      for restaurant in restaurant_seed_data:
        (Restaurant(**restaurant)).save()

    
