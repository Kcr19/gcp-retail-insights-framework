from faker import Faker

import json
import utils
import random

# Instantiate Faker
fake = Faker()


def po_line_data():
    """
    Generates fake data for the PO Line table
    :return: fake orders data
    """

    po_number = random.choice(utils.PO_NUMBER)
    po_line = random.choice(TEMP_PO_LINE_ID)
    if po_line in TEMP_PO_LINE_ID:
        TEMP_PO_LINE_ID.remove(str(po_line))

    # p = open('./outputs/ASNLine.json')
    # asn_line_data = json.load(p)
    # for j in asn_line_data:
    #     if po_number == j["PONumber"]:
    #         po_line = j["POLine"]

    ship_to_node = random.choice(TEMP_NODE_ID)
    product_id = random.choice(TEMP_PRODUCT_ID)
    order_quantity = int(''.join([random.choice('123456789') for _ in range(2)]))
    order_price = round(float(''.join([random.choice('123456789') for _ in range(2)])) * 1.1, 2)
    create_date = utils.get_create_date().isoformat()
    update_date = fake.past_datetime().isoformat()

    output = {
        "PONumber": po_number,
        "POLine": po_line,
        "ShipToNode": ship_to_node,
        "ProductId": product_id,
        "OrderQuantity": order_quantity,
        "OrderPrice": order_price,
        "CreateDate": create_date,
        "UpdateDate": update_date,
        "UpdateCount": 0
    }

    return output


def data_generator(count, po_line_ids, node_ids, product_ids):
    global TEMP_PO_LINE_ID, TEMP_NODE_ID, TEMP_PRODUCT_ID
    data = []
    
    TEMP_PO_LINE_ID = po_line_ids.copy()
    TEMP_NODE_ID = node_ids.copy()
    TEMP_PRODUCT_ID = product_ids.copy()

    # Generate data
    for _ in range(count):
        output = po_line_data()
        data.append(output)

    return data
