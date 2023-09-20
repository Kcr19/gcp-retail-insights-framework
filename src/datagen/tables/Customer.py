from faker import Faker

import json
import utils
import random

# Instantiate Faker
fake = Faker()

CUST_ID = []


def customer_data():
    """
    Generates fake data for the customer table
    :return: fake customer data
    """

    org_name = None
    loyalty_id = None
    loyalty_tier = None
    city = None
    state = None
    customer_zip = None
    country = None

    customer_id = random.choice(utils.CUSTOMER_ID)
    customer_type = random.choice(['B2B', 'B2C'])

    if customer_type == 'B2B':
        org_name = fake.company()

        loyalty_id = ''.join(random.sample(TEMP_LOYALTY_ID, 1))
        if loyalty_id in TEMP_LOYALTY_ID:
            TEMP_LOYALTY_ID.remove(str(loyalty_id))

        if loyalty_id != 1:
            loyalty_tier = random.choice(["Bronze", "Silver", "Gold", "Platinum", "Diamond"])

    create_date = utils.get_create_date().isoformat()
    update_date = fake.past_datetime().isoformat()

    pii_token = random.choice(utils.PII_TOKEN)

    # Get PII metadata from json
    f = open('./outputs/PII.json')
    data = json.load(f)
    for i in data:
        if pii_token == i["PIIToken"]:
            city = i["City"]
            state = i["State"]
            customer_zip = i["Zip"]
            country = i["Country"]
    CUST_ID.clear()

    # Build an output
    output = {
        "CustomerId": customer_id,
        "CustomerType": customer_type,
        "OrgName": org_name,
        "LoyaltyId": loyalty_id,
        "LoyaltyTier": loyalty_tier,
        "PIIToken": pii_token,
        "City": city,
        "State": state,
        "Zip": customer_zip,
        "Country": country,
        "CreateDate": create_date,
        "UpdateDate": update_date,
        "UpdateCount": 0
    }

    return output


def data_generator(count, node_ids, loyalty_ids):
    global TEMP_NODE_ID, TEMP_LOYALTY_ID
    data = []

    TEMP_NODE_ID = node_ids.copy()
    TEMP_LOYALTY_ID = loyalty_ids.copy()

    # Generate data
    for _ in range(count):
        output = customer_data()
        data.append(output)

    return data
