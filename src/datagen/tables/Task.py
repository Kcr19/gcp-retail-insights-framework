from faker import Faker

import utils
import random

# Instantiate Faker
fake = Faker()


def task_data():
    """
    Generates fake data for the task table
    :return: fake task data
    """
    equipment_lead_time_min = None

    task_id = fake.iban()
    effective_date = utils.get_create_date().isoformat()
    name = "task-name" + task_id
    work_unit = random.choice(["Minute", "Hour", "Day", "Month", "Year"])
    avg_duration = random.randint(1, 50)
    tier1 = random.randint(1, 5)
    tier2 = random.randint(1, 5)
    tier3 = random.randint(1, 5)
    tier4 = random.randint(1, 5)
    tier5 = random.randint(1, 5)
    equipment_type = random.choice(["None", "Machine", "Computer"])
    if equipment_type != "None":
        equipment_lead_time_min = random.randint(1, 60)
    create_date = utils.get_create_date().isoformat()
    update_date = fake.past_datetime().isoformat()

    # Build an output
    output = {
        "TaskId": task_id,
        "EffectiveDate": effective_date,
        "Name": name,
        "WorkUnit": work_unit,
        "AvgDuration": avg_duration,
        "Tier1Duration": tier1,
        "Tier2Duration": tier2,
        "Tier3Duration": tier3,
        "Tier4Duration": tier4,
        "Tier5Duration": tier5,
        "EquipmentType": equipment_type,
        "EquipmentLeadTimeMin": equipment_lead_time_min,
        "CreateDate": create_date,
        "UpdateDate": update_date,
        "UpdateCount": 0
    }

    return output


def data_generator(count):
    data = []

    # Generate data
    for _ in range(count):
        output = task_data()
        data.append(output)

    return data
