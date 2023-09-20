from faker import Faker

import uuid
import utils
import random

# Instantiate Faker
fake = Faker()


def pii_data():
    """
    Generates fake data for the PII table
    :return: fake PII data
    """

    pii_token = random.choice(TEMP_PII_TOKEN_ID)
    if pii_token in TEMP_PII_TOKEN_ID:
        TEMP_PII_TOKEN_ID.remove(str(pii_token))
    unique_id = str(uuid.uuid4())
    gender = random.choice(["Male", "Female"])
    if gender == "Male":
        first_name = fake.first_name_male()
        last_name = fake.last_name_male()
        pronoun = "he/him"
    else:
        first_name = fake.first_name_female()
        last_name = fake.last_name_female()
        pronoun = "she/her"
    race = random.choice(["White", "Black", "Alaska Native", "Asian", "Native Hawaiian"])
    email = fake.email()
    company = fake.company()
    ssn = fake.ssn()
    driving_license = fake.license_plate()
    dob = str(fake.date_of_birth())
    cell = fake.phone_number()
    address = fake.street_address()
    city = fake.city()
    state = fake.state()
    location_zip = fake.postcode()
    country = fake.current_country_code()
    device_serial_no = fake.unix_device()
    mac_address = fake.mac_address()
    ip_address = fake.ipv4()
    login_id = fake.safe_email()
    password = fake.password()
    pwd_last_change = fake.past_datetime().isoformat()
    create_date = utils.get_create_date().isoformat()
    update_date = fake.past_datetime().isoformat()

    # Build an output
    output = {
        "PIIToken": pii_token,
        "UniqueID": unique_id,
        "FirstName": first_name,
        "LastName": last_name,
        "Gender": gender,
        "Pronoun": pronoun,
        "Race": race,
        "Email": email,
        "Company": company,
        "SSN": ssn,
        "DriverLicense": driving_license,
        "DOB": dob,
        "Cell": cell,
        "Address1": address,
        "City": city,
        "State": state,
        "Zip": location_zip,
        "Country": country,
        "DeviceSerialNo": device_serial_no,
        "MACAddress": mac_address,
        "IPAddress": ip_address,
        "LoginID": login_id,
        "Password": password,
        "PwdLastChanged": pwd_last_change,
        "CreateDate": create_date,
        "UpdateDate": update_date,
        "UpdateCount": 0
    }

    return output


def data_generator(count, ids):
    global TEMP_PII_TOKEN_ID
    data = []

    TEMP_PII_TOKEN_ID = ids.copy()

    # Generate data
    for _ in range(count):
        output = pii_data()
        data.append(output)

    return data
