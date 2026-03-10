import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Esta magia encuentra la ruta exacta de tu archivo .env, 
# sin importar si lo corres tú o lo corre pytest
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

# Forzamos a cargar ese archivo específico
load_dotenv(dotenv_path=ENV_PATH)

def get_database() -> MongoClient:
    """
    Returns a database connection to the food database.

    :return: a PyMongo Client object representing the connection to the MongoDB server
    using the restaurant database
    """
    # Use your username and password to log in to MongoDB
    username = os.getenv("MONGO_USER")
    password = os.getenv("MONGO_PASS")
    
    # it should be in the following format: mongodb://<username>:<password>@<host>:<port>/
    CONNECTION_STRING = f"mongodb://{username}:{password}@localhost:27017/"
    
    # Create a connection using MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database (if it does not exist) and return it
    # 😎 The MongoClient class has a dictionary-like interface for accessing databases
    return client["restaurant"]


if __name__ == "__main__":
    # Print the database connection
    print(get_database())
    print("Database connection successful!")