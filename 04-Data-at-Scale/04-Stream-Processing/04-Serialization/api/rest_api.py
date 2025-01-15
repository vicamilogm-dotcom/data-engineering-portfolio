# IMPORT YOUR PACKAGES HERE

from api import rural

# Create an `app` variable with the correct FastAPI object
# YOUR CODE HERE


pass  # YOUR CODE HERE
def time() -> dict:
    """Get the current time using the datetime module.
    Use the hour, minute and second attributes of the datetime object.

    Returns:
        dict: A dictionary containing the current time in the format
              {'h': HH, 'm': MM, 's': SS}
    """

    # Replace `dt = None` with the current time
    pass  # YOUR CODE HERE


pass  # YOUR CODE HERE
def get_rural_population(country: str, year: int):
    df = rural.load_rural_csv()
    # Fill the `value` of the rural population percentage for the input country and year
    value = 0
    pass  # YOUR CODE HERE
    return {"rural_pop_perc": value}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
