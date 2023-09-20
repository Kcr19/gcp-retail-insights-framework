from faker import Faker

import utils
import random

# Instantiate Faker
fake = Faker()


def associate_data():
    """
    Generates fake data for the Associate table
    :return: fake Associate data
    """

    associate_id = random.choice(TEMP_ASSOCIATE_ID)
    if associate_id in TEMP_ASSOCIATE_ID:
        TEMP_ASSOCIATE_ID.remove(str(associate_id))
    effective_date = utils.get_create_date().isoformat()
    pii_token = random.choice(utils.PII_TOKEN)
    skill_tier = random.choice(["Novice", "Trainee", "Beginner", "Experienced", "Expert"])
    avg_rate_min = round(random.randint(1, 10) * 1.1, 2)
    create_date = utils.get_create_date().isoformat()
    update_date = fake.past_datetime().isoformat()

    # Build an output
    output = {
        "AssociateId": associate_id,
        "EffectiveDate": effective_date,
        "PIIToken": pii_token,
        "SkillTier": skill_tier,
        "AvgRateMin": avg_rate_min,
        "CreateDate": create_date,
        "UpdateDate": update_date,
        "UpdateCount": 0
    }

    return output


def data_generator(count, ids):
    global TEMP_ASSOCIATE_ID
    data = []

    TEMP_ASSOCIATE_ID = ids.copy()

    # Generate data
    for _ in range(count):
        output = associate_data()
        data.append(output)

    return data
