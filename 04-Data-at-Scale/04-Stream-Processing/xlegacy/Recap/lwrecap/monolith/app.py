from fastapi import FastAPI

from lwrecap.monolith import business_logic

app = FastAPI()


@app.get("/users")
def users():
    """
    List all the users in the app
    """
    return {
        "users": [
            {"id": 1, "name": "John Smith", "email": "john@gmail.com"},
            {"id": 2, "name": "Becca Hey", "email": "becca@gmail.com"},
            {"id": 3, "name": "Doro Tea", "email": "doro@gmail.com"},
        ]
    }


@app.get("/companies/:company_id/products")
def products(company_id: int):
    """
    Lists all the products for a given company
    """
    return {
        "products": [
            {"id": 1, "name": "Headphones", "sku": "ABC123"},
            {"id": 2, "name": "USB cable", "email": "ABC137"},
        ]
    }


@app.post("/life-cycle-calculation")
def lca(payload):
    lca_result = business_logic.compute_lca(payload)
    return lca_result
