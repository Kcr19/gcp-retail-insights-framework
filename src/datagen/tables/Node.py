from faker import Faker

import json
import utils
import random

# Instantiate Faker
fake = Faker(['en_US'])


def node_data():
    """
    Generates fake data for the node table
    :return: fake node data
    """
    node_values = random.choice(["DC", "STORE"])
    id = random.choice(TEMP_NODE_ID)
    node_id = node_values + id
    if id in TEMP_NODE_ID:
        TEMP_NODE_ID.remove(str(id))
    node_name = node_id+'-'+fake.state()
    if node_values == 'DC':
        node_type = random.choice(["DC", "RDC", "MFDC", "FDC", "Digital"])
    else:
        node_type = 'Store'
    layout_id = random.choice(utils.LAYOUT_ID)
    range_cluster = 'rzone0'+str(random.randint(1, 6))
    price_cluster = 'pzone0'+str(random.randint(1, 6))
    gln_number = "gln-"+''.join([random.choice('0123456789') for _ in range(13)])
    location_zip = fake.postcode()
    location_country = fake.current_country_code()
    avg_mon_store_traffic = random.randrange(1000, 9999)
    avg_labor_cost = round(random.randint(7, 25) * 1.1, 2)
    create_date = utils.get_create_date().isoformat()
    update_date = fake.past_datetime().isoformat()

    # Get layout metadata from json
    f = open('./outputs/NodeLayout.json')
    data = json.load(f)
    for i in data:
        node_back_store_capacity = None
        node_shelf_capacity = None
        if layout_id == i["LayId"]:
            if i["DisplayLoc"] == "False":
                node_back_store_capacity = round(random.randint(1, 80) * 1.1, 2)
            else:
                node_shelf_capacity = round(random.randint(1, 80) * 1.1, 2)

            # Build an output
            output = {
                "NodeId": node_id,
                "Name": node_name,
                "Type": node_type,
                "LayId": layout_id,
                "RangeCluster": range_cluster,
                "PriceCluster": price_cluster,
                "GLNNumber": gln_number,
                "Zip": location_zip,
                "Country": location_country,
                "AvgMonthStoreTraffic": avg_mon_store_traffic,
                "NodeShelfCapacity": node_shelf_capacity,
                "NodeBackStoreCapacity": node_back_store_capacity,
                "AverageLaborCostHour": avg_labor_cost,
                "CreateDate": create_date,
                "UpdateDate": update_date,
                "UpdateCount": 0
            }

            return output


def data_generator(count, ids):
    global TEMP_NODE_ID
    data = []

    TEMP_NODE_ID = ids.copy()

    # Generate data
    for _ in range(count):
        output = node_data()
        data.append(output)

    return data
