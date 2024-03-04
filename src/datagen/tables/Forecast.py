from faker import Faker
import datetime as dt

import json
import utils
import random

# Instantiate Faker
fake = Faker()
NODE_ID = []
FORECAST_ID = []


def forecast_data():
    """
    Generates fake data for the inventory table
    :return: fake inventory data
    """

    product_id = random.choice(TEMP_PRODUCT_ID)

    fcst_id = random.choice(FORECAST_ID)
    FORECAST_ID.remove(fcst_id)

    location_node = random.choice(NODE_ID)
    fcst_date = utils.get_random_future_date().isoformat()
    quantity = random.randrange(0,1000,100)

    # Build an output
    output = {
        "ForecastId": fcst_id,
        "LocationNode": location_node,
        "ProductId": product_id,
        "DemandDate": fcst_date,
        "Quantity": quantity,
    }

    return output


def data_generator(count, fcst_ids, prod_ids):
    global TEMP_PRODUCT_ID
    global FORECAST_ID
    data = []

    # Get Node metadata from node.json
    f = open('./outputs/RefNode.json')
    json_data = json.load(f)
    for i in json_data:
        if i['NodeId'].startswith('DC'):
            NODE_ID.append(i['NodeId'])

    TEMP_PRODUCT_ID = prod_ids.copy()
    FORECAST_ID = fcst_ids.copy()

    # Generate data
    for _ in range(count):
        output = forecast_data()
        data.append(output)

    return data
