from faker import Faker
import datetime as dt

import json
import utils
import random

# Instantiate Faker
fake = Faker()
FN = []
STR = []
PRD_ID = []


def replenishment_data():
    """
    Generates fake data for the replenishment table
    :return: fake replenishment data
    """

    product_id = random.choice(TEMP_PRODUCT_ID)
    if product_id in TEMP_PRODUCT_ID:
        TEMP_PRODUCT_ID.remove(str(product_id))
    PRD_ID.append(product_id)

    # Get Node metadata from node.json
    f = open('./outputs/RefNode.json')
    json_data = json.load(f)
    for i in json_data:
        if i['Type'] == 'DC':
            FN.append(i['NodeId'])
        elif i['Type'] == 'Store':
            STR.append(i['NodeId'])
        else:
            None

    from_node = random.choice(FN)
    to_node = random.choice(STR)
    effective_date = utils.get_create_date().isoformat()
    replenish_frequency = random.choice(["Daily", "Weekly", "BiWeekly", "Monthly", "Seasonally", "Yearly"])
    year_schedule = dt.date.today().year
    mon_schedule = random.choice(['Yes', 'No'])
    tue_schedule = random.choice(['Yes', 'No'])
    wed_schedule = random.choice(['Yes', 'No'])
    thu_schedule = random.choice(['Yes', 'No'])
    fri_schedule = random.choice(['Yes', 'No'])
    sat_schedule = random.choice(['Yes', 'No'])
    sun_schedule = random.choice(['Yes', 'No'])
    bi_weekly_WoM = random.randint(1, 9)
    monthly_DoM = random.randint(1, 9)
    create_date = utils.get_create_date().isoformat()
    update_date = fake.past_datetime().isoformat()

    # Build an output
    output = {
        "FromNode": from_node,
        "ToNode": to_node,
        "ProductId": product_id,
        "EffectiveDate": effective_date,
        "ReplenishFrequency": replenish_frequency,
        "YearSchedule": year_schedule,
        "MonSchedule": mon_schedule,
        "TueSchedule": tue_schedule,
        "WedSchedule": wed_schedule,
        "ThuSchedule": thu_schedule,
        "FriSchedule": fri_schedule,
        "SatSchedule": sat_schedule,
        "SunSchedule": sun_schedule,
        "BiWeeklyWoM": bi_weekly_WoM,
        "MonthlyDoM": monthly_DoM,
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
        output = replenishment_data()
        data.append(output)

    return data
