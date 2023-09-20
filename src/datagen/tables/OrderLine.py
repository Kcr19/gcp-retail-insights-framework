from faker import Faker

import utils
import random

# Instantiate Faker
fake = Faker()


def orders_line_data():
    """
    Generates fake data for the orders line table
    :return: fake orders line data
    """

    order_id = random.choice(TEMP_ORDER_ID)
    if order_id in TEMP_ORDER_ID:
        TEMP_ORDER_ID.remove(str(order_id))

    product_id = random.choice(TEMP_PRODUCT_ID)
    if product_id in TEMP_PRODUCT_ID:
        TEMP_PRODUCT_ID.remove(str(product_id))

    order_line = ''.join([random.choice('123456789') for _ in range(6)])
    selling_price = round(random.randint(1, 99) * 1.1, 2)
    order_quantity = int(''.join([random.choice('123456789') for _ in range(2)]))
    promised_quantity = int(''.join([random.choice('123456789') for _ in range(2)]))
    delivered_quantity = int(''.join([random.choice('123456789') for _ in range(2)]))
    line_gross_amount = round(float(''.join([random.choice('123456789') for _ in range(2)])) * 1.1, 2)
    line_tax_amount = int(line_gross_amount) * int(''.join([random.choice('12') for _ in range(1)])) / 10
    line_discount_amount = round(
        (line_gross_amount + line_tax_amount) * int(''.join([random.choice('123') for _ in range(1)])) / 10, 2)
    line_net_amount = round((line_gross_amount + line_tax_amount) - line_discount_amount, 2)
    create_date = utils.get_create_date().isoformat()
    update_date = fake.past_datetime().isoformat()

    if promised_quantity < delivered_quantity:
        promised_quantity = delivered_quantity + random.randint(1, 9)
    else:
        promised_quantity = promised_quantity

    # Make sure: Order Quantity > Promised Quantity > delivered Quantity
    if order_quantity < promised_quantity or order_quantity < delivered_quantity:
        if order_quantity < promised_quantity:
            edited_order_quantity = promised_quantity + random.randint(1, 9)
        else:
            edited_order_quantity = delivered_quantity + random.randint(1, 9)
    else:
        edited_order_quantity = order_quantity
    
    
    

    # Build an output
    output = {
        "OrderId": order_id,
        "OrderLine": order_line,
        "ProductId": product_id,
        "SellingPrice": selling_price,
        "OrderQuantity": edited_order_quantity,
        "PromisedQuantity": promised_quantity,
        "DeliveredQuantity": delivered_quantity,
        "LineGrossAmount": line_gross_amount,
        "LineTaxAmount": line_tax_amount,
        "LineDiscountAmount": line_discount_amount,
        "LineNetAmount": line_net_amount,
        "CreateDate": create_date,
        "UpdateDate": update_date,
        "UpdateCount": 0
    }

    return output


def data_generator(count, order_ids, product_ids):
    global TEMP_ORDER_ID, TEMP_PRODUCT_ID
    data = []

    TEMP_ORDER_ID = order_ids.copy()
    TEMP_PRODUCT_ID = product_ids.copy()

    # Generate data
    for _ in range(count):
        output = orders_line_data()
        data.append(output)

    return data
