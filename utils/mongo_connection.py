from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
CONNECTION_STATUS = False

def connect_to_mongodb():
    global CONNECTION_STATUS
    if CONNECTION_STATUS == False:
        uri = "mongodb+srv://airlinetest:airlinetest@airlinesapp.izaoc4c.mongodb.net/"
        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi("1"))
        # Send a ping to confirm a successful connection
        try:
            client.admin.command("ping")
            CONNECTION_STATUS = True
            return "Pinged your deployment. You successfully connected to MongoDB!"

        except Exception as e:
            print(e)
    else:
        return "Alredy connected to MongoDB!"
