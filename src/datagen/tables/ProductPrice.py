from faker import Faker

import utils
import random

# Instantiate Faker
fake = Faker()


def product_price_data():
    """
    Generates fake data for the product_price table
    :return: fake product_price data
    """

    product_id = random.choice(utils.PRODUCT_ID)
    node_id = random.choice(utils.NODE_ID)
    effective_date = utils.get_create_date().isoformat()
    cost_price = round(random.randrange(1, 100) * 1.1, 2)
    base_price = round(random.randrange(1, 12) * 1.1, 2)
    selling_price = base_price + cost_price

    create_date = utils.get_create_date().isoformat()
    update_date = fake.past_datetime().isoformat()

    # Build an output
    output = {
        "ProductId": product_id,
        "NodeId": node_id,
        "EffectiveDate": effective_date,
        "CostPrice": cost_price,
        "BasePrice": base_price,
        "SellingPrice": selling_price,
        "CreateDate": create_date,
        "UpdateDate": update_date,
        "UpdateCount": 0
    }

    return output


def data_generator(count):
    data = []

    # Generate data
    for _ in range(count):
        output = product_price_data()
        data.append(output)

    return data
