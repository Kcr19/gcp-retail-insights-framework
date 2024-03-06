from faker import Faker
import datetime as dt

import json
import utils
import random

# Instantiate Faker
fake = Faker()
NODE_ID = []
INVENTORY_ID = []


def inventory_data():
    """
    Generates fake data for the inventory table
    :return: fake inventory data
    """
    inventory_id = random.choice(INVENTORY_ID)
    INVENTORY_ID.remove(inventory_id)

    product_id = random.choice(TEMP_PRODUCT_ID)


    location_node = random.choice(NODE_ID)
    product = product_id
    manufactured_date = utils.get_create_date().isoformat()
    quantity = random.randrange(0,1000,100)

    # Build an output
    output = {
        "InventoryId": inventory_id,
        "LocationNode": location_node,
        "ProductId": product_id,
        "MfgDate": manufactured_date,
        "Quantity": quantity,
    }

    return output


def data_generator(count, inv_ids, prod_ids):
    global TEMP_PRODUCT_ID
    global INVENTORY_ID
    data = []

    # Get Node metadata from node.json
    f = open('./outputs/RefNode.json')
    json_data = json.load(f)
    for i in json_data:
        if i['NodeId'].startswith('DC'):
            NODE_ID.append(i['NodeId'])

    TEMP_PRODUCT_ID = prod_ids.copy()
    INVENTORY_ID = inv_ids.copy()

    # Generate data
    for _ in range(count):
        output = inventory_data()
        data.append(output)

    return data
