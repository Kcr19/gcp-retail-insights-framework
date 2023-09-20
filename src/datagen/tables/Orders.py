from faker import Faker

import json
import uuid
import utils
import random

# Instantiate Faker
fake = Faker()
STORE_ID = []


def orders_data():
    """
    Generates fake data for the orders table
    :return: fake orders data
    """
    loyalty_tier = None
    loyalty_id = None

    customer_id = random.choice(TEMP_CUST_ID)

    # Get Customer metadata from Customer.json
    c = open('./outputs/RefCustomer.json')
    customer_json_data = json.load(c)
    for j in customer_json_data:
        if customer_id == j['CustomerId']:
            loyalty_id = j['LoyaltyId']
            loyalty_tier = j['LoyaltyTier']

    # Get Node metadata from Node.json
    f = open('./outputs/RefNode.json')
    json_data = json.load(f)
    for i in json_data:
        if i['Type'] == 'Store':
            STORE_ID.append(i['NodeId'])

    order_id = random.choice(TEMP_ORDER_ID)
    if order_id in TEMP_ORDER_ID:
        TEMP_ORDER_ID.remove(str(order_id))
    order_type = random.choice(["Sales", "PO", "ASN", "Transfer", "Return", "Service"])
    order_date = utils.get_create_date().isoformat()
    channel = random.choice(["Store", "Web", "Mobile", "Kiosk", "Marketplace"])
    node_id = random.choice(STORE_ID)
    ship_to_city = fake.city()
    ship_to_state = fake.state()
    ship_to_zip = fake.postcode()
    order_status = random.choice(["Completed", "Closed", "Returned", "Cancelled"])
    gross_amount = round(float(''.join([random.choice('123456789') for _ in range(2)])) * 1.1, 2)
    tax_amount = int(gross_amount) * int(''.join([random.choice('12') for _ in range(1)])) / 10
    discount_amount = round((gross_amount + tax_amount) * int(''.join([random.choice('123') for _ in range(1)])) / 10, 2)
    net_amount = round((gross_amount + tax_amount) - discount_amount, 2)
    associate_id = random.choice(TEMP_CUST_ID)
    transaction_id = "TXID-" + ''.join([random.choice('0123456789') for _ in range(8)])
    parcel_id = "PRCLID-" + str(uuid.uuid1().node)
    create_date = utils.get_create_date().isoformat()
    update_date = fake.past_datetime().isoformat()

    # Build an output
    output = {
        "OrderId": order_id,
        "Type": order_type,
        "OrderDate": order_date,
        "Channel": channel,
        "NodeId": node_id,
        "CustomerId": customer_id,
        "LoyaltyId": loyalty_id,
        "LoyaltyTier": loyalty_tier,
        "ShipToCity": ship_to_city,
        "ShipToState": ship_to_state,
        "ShipToZip": ship_to_zip,
        "OrderStatus": order_status,
        "GrossAmount": gross_amount,
        "TaxAmount": tax_amount,
        "DiscountAmount": discount_amount,
        "NetAmount": net_amount,
        "AssociateId": associate_id,
        "TransactionId": transaction_id,
        "ParcelId": parcel_id,
        "CreateDate": create_date,
        "UpdateDate": update_date,
        "UpdateCount": 0
    }

    return output


def data_generator(count, order_ids, customer_ids, associate_ids):
    global TEMP_ORDER_ID, TEMP_CUST_ID, TEMP_ASSOC_ID
    data = []

    TEMP_ORDER_ID = order_ids.copy()
    TEMP_CUST_ID = customer_ids.copy()
    TEMP_ASSOC_ID = associate_ids.copy()

    # Generate data
    for _ in range(count):
        output = orders_data()
        data.append(output)

    return data
