from faker import Faker
from datetime import datetime

import json
import utils
import random
import datetime as dt

# Instantiate Faker
fake = Faker()

NODE_ID = []
SUPPLIER_ID = []


def po_data():
    """
    Generates fake data for the PO table
    :return: fake PO data
    """

    # Get Node metadata from json
    f = open('./outputs/RefNode.json')
    data = json.load(f)
    for i in data:
        if i["Type"] == 'Store' or i["Type"] == 'DC':
            NODE_ID.append(i["NodeId"])

    t = open('./outputs/RefTradePartner.json')
    trade_data = json.load(t)
    for j in trade_data:
        if j["PartnerType"] == 'Supplier':
            SUPPLIER_ID.append(j["TradePartnerId"])

    po_number = random.choice(TEMP_PO_NUMBER_ID)
    if po_number in TEMP_PO_NUMBER_ID:
        TEMP_PO_NUMBER_ID.remove(str(po_number))
    po_type = random.choice(["Standard", "Blanket", "Consolidated"])
    ship_to_node = random.choice(NODE_ID)
    order_date = utils.get_create_date().isoformat()
    convert_date = datetime.fromisoformat(order_date)
    earlier_ship_date = datetime.strptime(str(convert_date), "%Y-%m-%d %H:%M:%S.%f") + dt.timedelta(
        days=random.randint(1, 20))
    latest_ship_date = datetime.strptime(str(convert_date), "%Y-%m-%d %H:%M:%S.%f") + dt.timedelta(
        days=random.randint(5, 10))
    supplier_id = random.choice(SUPPLIER_ID)
    status = random.choice(["Create", "Open", "Approve", "Sent", "Acknowledge", "Deliver", "Complete", "PartialComplete", "Reject", "Cancel", "Close"])
    gross_amount = round(float(''.join([random.choice('123456789') for _ in range(2)])) * 1.1, 2)
    tax_amount = int(gross_amount) * int(''.join([random.choice('12') for _ in range(1)])) / 10
    discount_amount = round((gross_amount + tax_amount) * int(''.join([random.choice('123') for _ in range(1)])) / 10,
                            2)
    net_amount = round((gross_amount + tax_amount) - discount_amount, 2)
    create_date = utils.get_create_date().isoformat()
    update_date = fake.past_datetime().isoformat()

    # Build an output
    output = {
        "PONumber": po_number,
        "POType": po_type,
        "OrderDate": order_date,
        "EarliestShipDate": earlier_ship_date.isoformat(),
        "LatestShipDate": latest_ship_date.isoformat(),
        "SupplierId": supplier_id,
        "ShipToNode": ship_to_node,
        "Status": status,
        "GrossAmount": gross_amount,
        "TaxAmount": tax_amount,
        "DiscountAmount": discount_amount,
        "NetAmount": net_amount,
        "CreateDate": create_date,
        "UpdateDate": update_date,
        "UpdateCount": 0
    }

    return output


def data_generator(count, ids):
    global TEMP_PO_NUMBER_ID
    data = []

    TEMP_PO_NUMBER_ID = ids.copy()

    # Generate data
    for _ in range(count):
        output = po_data()
        data.append(output)

    return data
