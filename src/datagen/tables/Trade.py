from faker import Faker

import json
import utils
import random

# Instantiate Faker
fake = Faker()


def trade_partner_data():
    """
    Generates fake data for the Trade Partner table
    :return: fake orders data
    """

    trade_partner_id = random.choice(TEMP_TRADE_PARTNER_ID)
    if trade_partner_id in TEMP_TRADE_PARTNER_ID:
        TEMP_TRADE_PARTNER_ID.remove(str(trade_partner_id))
    partner_type = random.choice(["Agent", "Carrier", "Supplier", "Shipper", "Wholesaler", "Manufacturer"])
    pii_token = random.choice(utils.PII_TOKEN)
    gln_number = "gln-" + ''.join([random.choice('0123456789') for _ in range(13)])
    qc_rating = round(random.randint(1, 5) * 1.1, 2)
    create_date = utils.get_create_date().isoformat()
    update_date = fake.past_datetime().isoformat()
    f = open('./outputs/PII.json')
    data = json.load(f)
    for i in data:
        if pii_token == i["PIIToken"]:
            pii_token_zip = i["Zip"]
            country = i["Country"]

            # Build an output
            output = {
                "TradePartnerId": trade_partner_id,
                "PartnerType": partner_type,
                "PIIToken": pii_token,
                "GLNNumber": gln_number,
                "QCRating": qc_rating,
                "Zip": pii_token_zip,
                "Country": country,
                "CreateDate": create_date,
                "UpdateDate": update_date,
                "UpdateCount": 0
            }

            return output


def data_generator(count, ids):
    global TEMP_TRADE_PARTNER_ID
    data = []

    TEMP_TRADE_PARTNER_ID = ids.copy()

    # Generate data
    for _ in range(count):
        output = trade_partner_data()
        data.append(output)

    return data
