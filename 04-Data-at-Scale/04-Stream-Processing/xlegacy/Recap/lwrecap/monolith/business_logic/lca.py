import time


def compute_lca():
    """
    Some expensive calculation is happening here, each call of this function takes up to 5 minutes
    """
    time.sleep(60 * 5)

    return {
        "impacts": {
            "global_warming": {"unit": "kg CO2 eq", "value": 10},
            "freshwater_eutrophication": {"unit": "kg PO43- eq", "value": 1.3},
        }
    }
