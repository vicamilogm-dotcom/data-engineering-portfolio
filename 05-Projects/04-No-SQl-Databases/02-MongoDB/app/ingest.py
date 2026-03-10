from pymongo.collection import Collection
from app.pymongo_get_database import get_database

db = get_database()

# create a new collection called "customers"
# assign it to the variable "customers"
customers = db["customers"]


# Insert the documents into the "customers" collection
def ingest_data(customers: Collection) -> None:
    """Ingest data into the customers collection."""
    # Create a collection named `customers` and insert the following documents
    docs = [
        { "name": "John Doe", "age": 35, "gender": "male", "address": "123 Main St" },
        { "name": "Jane Smith", "age": 28, "gender": "female", "address": "456 Park Ave" },
        { "name": "Michael Johnson", "age": 41, "gender": "male", "address": "789 Oak St" }
    ]
    customers.insert_many(docs)


if __name__ == "__main__":
    # Limpiamos la colección primero para evitar duplicados si ejecutamos esto varias veces
    customers.drop()
    
    ingest_data(customers)

    # Count the number of documents in the "customers" collection
    total_customer = customers.count_documents({})
    print(f"There are now {total_customer} customers in the collection.")