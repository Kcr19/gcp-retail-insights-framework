import json
import random
import datetime as dt
from datetime import datetime

FINAL_DATA = []
PO_NUMBERS = []
STATUS = ["Open", "Reviewing", ["Approved", "Rejected"], "Sent", "Received", "Shipped", "On Hold", "In Transit", "Delivering"]

# Get today's date and time
now = datetime.today()
approve_deny_status = None


def po_update_data():
    # Get PO data
    f = open('./outputs/PO.json')
    po_data = json.load(f)
    for i in po_data:
        po = i["PONumber"]
        PO_NUMBERS.append(po)

    # Get POLine data
    f = open('./outputs/POLine.json')
    poline_data = json.load(f)

    for po_number in PO_NUMBERS:
        for i in poline_data:
            if po_number in i["PONumber"]:
                update_date = now - dt.timedelta(days=random.randint(1, 1000), hours=random.randint(1, 60), 
                minutes=random.randint(1, 59), milliseconds=random.randint(000000, 999999))
                create_date = update_date - dt.timedelta(days=random.randint(1, 100), hours=random.randint(1, 60), 
                minutes=random.randint(1, 59), milliseconds=random.randint(000000, 999999))
                entry_date = create_date - dt.timedelta(minutes=random.randint(1, 59), 
                milliseconds=random.randint(000000, 999999))
                for each_status in STATUS[0:random.randint(3, 9)]:
                    if type(each_status) is not list:
                        if each_status == "Open":
                            po_line = i['POLine']
                            output_dict = {
                            "PONumber": po_number,
                            "POLine": po_line,
                            "Status": each_status,
                            "CreateDate": create_date.isoformat(),
                            "EntryDate": entry_date.isoformat(),
                            "UpdateDate": update_date.isoformat()
                            }
                            FINAL_DATA.append(output_dict)
                        else:
                            temp_date = update_date
                            update_date = temp_date + dt.timedelta(days=random.randint(1, 100), hours=random.randint(1, 60), 
                            minutes=random.randint(1, 59), milliseconds=random.randint(000000, 999999))
                            output_dict = {
                            "PONumber": po_number,
                            "POLine": po_line,
                            "Status": each_status,
                            "CreateDate": create_date.isoformat(),
                            "EntryDate": entry_date.isoformat(),
                            "UpdateDate": update_date.isoformat()
                            }
                            FINAL_DATA.append(output_dict)
                    else:
                        each_status = random.choice(each_status)
                        temp_date = update_date
                        update_date = temp_date + dt.timedelta(days=random.randint(1, 100), hours=random.randint(1, 60), 
                        minutes=random.randint(1, 59), milliseconds=random.randint(000000, 999999))
                        output_dict = {
                            "PONumber": po_number,
                            "POLine": po_line,
                            "Status": each_status,
                            "CreateDate": create_date.isoformat(),
                            "EntryDate": entry_date.isoformat(),
                            "UpdateDate": update_date.isoformat()
                            }
                        FINAL_DATA.append(output_dict)
                        if each_status == "Rejected":
                            break

    return FINAL_DATA