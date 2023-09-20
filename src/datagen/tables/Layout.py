from faker import Faker

import utils
import random

# Instantiate Faker
fake = Faker()


def layout_data():
    """
    Generates fake data for the layout table
    :return: fake layout data
    """

    layout_id = random.choice(TEMP_LAYOUT_ID)
    if layout_id in TEMP_LAYOUT_ID:
        TEMP_LAYOUT_ID.remove(str(layout_id))
    layout_name = fake.iban()
    zone = "Z"+str(random.randint(1, 10))
    aisle = "A"+str(random.randint(1, 10))
    bay = "B"+str(random.randint(1, 25))
    level = "L"+str(random.randint(1, 8))
    slot = "S"+str(random.randint(1, 20))
    display_location = random.choice(["True", "False"])
    capacity = round(random.randint(1, 20) * 1.1, 2)
    create_date = utils.get_create_date().isoformat()
    update_date = fake.past_datetime().isoformat()

    # Build an output
    output = {
        "LayId": layout_id,
        "Name": layout_name,
        "Zone": zone,
        "Aisle": aisle,
        "Bay": bay,
        "Level": level,
        "Slot": slot,
        "DisplayLoc": display_location,
        "Capacity": capacity,
        "PickTravelSequence": None,
        "StockTravelSequence": None,
        "CreateDate": create_date,
        "UpdateDate": update_date,
        "UpdateCount": 0
    }

    return output


def data_generator(count, ids):
    global TEMP_LAYOUT_ID
    data = []

    TEMP_LAYOUT_ID = ids.copy()

    # Generate data
    for _ in range(count):
        output = layout_data()
        data.append(output)

    return data
