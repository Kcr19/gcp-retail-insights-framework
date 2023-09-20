from faker import Faker
from random import randrange

import utils
import random
import faker_commerce

# Instantiate Faker
fake = Faker()
fake.add_provider(faker_commerce.Provider)


def product_data():
    """
    Generates fake data for the product table
    :return: fake product data
    """

    style = None
    color = None
    size = None
    brand = None
    model = None
    model_year = None

    product_id = random.choice(TEMP_PRODUCT_ID)
    if product_id in TEMP_PRODUCT_ID:
        TEMP_PRODUCT_ID.remove(str(product_id))
    effective_date = utils.get_create_date().isoformat()
    name = fake.ecommerce_name()
    default_cost_price = round(10 * 1.12, 2)
    default_base_price = round(3 * 1.1, 2)
    default_selling_price = round(15 * 1.1, 2)
    gpc_segment = random.choice(["seg-70000000", "seg-68000000", "seg-53000000"])
    gpc_family = random.choice(["fam-70010000", "fam-68010000", "fam-53010000"])
    gpc_class = random.choice(["cls-70010200", "cls-68010700", "cls-53220100"])
    gcp_brick = random.choice(["brick-10001686", "brick-10005726", "brick-10000666"])
    division = random.choice(['A', 'B', 'C', 'D', 'F'])
    department = random.choice(["stores", "finance", "marketing", "sales", "merchandising"])
    product_class = random.choice(["Apparel", "Consumer electronics"])

    if product_class == "Apparel":
        style = random.choice(["80's", "summer", "winter", "spring"])
        color = random.choice(["blue", "green", "yellow", "white", "red", "purple"])
        size = random.choice(["xs", "s", "m", "l", "xl", "2xl", "3xl"])
    else:
        brand = random.choice(["brand-A", "brand-B", "brand-C", "brand-D"])
        model = random.choice(["model-A", "model-B", "model-C", "model-D", "model-E", "model-F"])
        model_year = utils.get_year()

    product_intro_date = utils.get_create_date().isoformat()
    trade_partner_id = random.choice(utils.TRADE_PARTNER_ID)
    upc = "upc--" + ''.join([random.choice('0123456789') for _ in range(12)])
    gtin_number = "gtin-" + ''.join([random.choice('0123456789') for _ in range(12)])
    mpn_number = "mpn-" + ''.join([random.choice('0123456789ABCEDF') for _ in range(7)])
    plu_code = "plu-" + ''.join([random.choice('0123456789') for _ in range(4)])
    buy_uom = random.choice(["PALLET", "CASE"])
    move_uom = random.choice(["TOTE", "CASE"])
    sell_uom = "EACHES"
    target_gender = random.choice(["All", "Male", "Female"])
    prepack_quantity = random.randrange(50, 100)
    inner_pack_quantity = random.choice([prepack_quantity, prepack_quantity - random.randrange(0, 20)])
    hazmat_class = random.randrange(1, 9)

    is_perishable = random.choice(["TRUE", "FALSE"])
    is_temprature_controled = random.choice(["TRUE", "FALSE"])
    is_durable = random.choice(["TRUE", "FALSE"])
    is_soft_goods = random.choice(["TRUE", "FALSE"])
    is_virtual = random.choice(["TRUE", "FALSE"])
    is_conveyable = random.choice(["TRUE", "FALSE"])
    is_serialized = random.choice(["TRUE", "FALSE"])
    is_wICEligible = random.choice(["TRUE", "FALSE"])
    is_fragile = random.choice(["TRUE", "FALSE"])
    tare_height = round(randrange(10, 30) * 1.1, 2)
    tare_width = round(randrange(10, 30) * 1.1, 2)
    tare_length = round(randrange(10, 30) * 1.1, 2)
    tare_weight = round(randrange(20, 50) * 1.1, 2)
    package_height = round(randrange(10, 30) * 1.1, 2)
    package_width = round(randrange(10, 30) * 1.1, 2)
    package_length = round(randrange(10, 30) * 1.1, 2)
    package_weight = round(randrange(10, 30) * 1.1, 2)
    landed_cost = round(randrange(10, 30) * 1.1, 2)
    create_date = utils.get_create_date().isoformat()
    update_date = fake.past_datetime().isoformat()

    # Build an output
    output = {
        "ProductId": product_id,
        "EffectiveDate": effective_date,
        "Name": name,
        "DefaultCostPrice": default_cost_price,
        "DefaultBasePrice": default_base_price,
        "DefaultSellingPrice": default_selling_price,
        "GPCSegment": gpc_segment,
        "GPCFamily": gpc_family,
        "GPCClass": gpc_class,
        "GPCBrick": gcp_brick,
        "Division": division,
        "Department": department,
        "Class": product_class,
        "Style": style,
        "Color": color,
        "Size": size,
        "Brand": brand,
        "Model": model,
        "ModelYear": model_year,
        "ProductIntroDate": product_intro_date,
        "TradePartnerId": trade_partner_id,
        "UPC": upc,
        "GTINNumber": gtin_number,
        "MPNNumber": mpn_number,
        "PLUCode": plu_code,
        "BuyUom": "buy-uom-"+str(buy_uom),
        "MoveUom": "move-uom-"+str(move_uom),
        "SellUom": sell_uom,
        "TargetGender": target_gender,
        "PrepackQuantity": prepack_quantity,
        "InnerPackQuantity": inner_pack_quantity,
        "HazmatClass": hazmat_class,
        "IsPerishable": is_perishable,
        "IsTempratureControlled": is_temprature_controled,
        "IsDurable": is_durable,
        "IsSoftGoods": is_soft_goods,
        "IsVirtual": is_virtual,
        "IsConveyable": is_conveyable,
        "IsSerialized": is_serialized,
        "IsWICEligible": is_wICEligible,
        "IsFragile": is_fragile,
        "TareHeight": tare_height,
        "TareWidth": tare_width,
        "TareLength": tare_length,
        "TareWeight": tare_weight,
        "PackageHeight": package_height,
        "PackageWidth": package_width,
        "PackageLength": package_length,
        "PackageWeight": package_weight,
        "LandedCost": landed_cost,
        "CreateDate": create_date,
        "UpdateDate": update_date,
        "UpdateCount": 0
    }

    return output


def data_generator(count, ids):
    global TEMP_PRODUCT_ID
    data = []

    TEMP_PRODUCT_ID = ids.copy()

    # Generate data
    for _ in range(count):
        output = product_data()
        data.append(output)

    return data
