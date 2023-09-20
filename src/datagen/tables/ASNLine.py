import json
import random
import utils

from faker import Faker

ASN = []
PO_LINE = []
FINAL = []

# Instantiate Faker
fake = Faker()

def run(PO_NUMBER, PRODUCT_ID):

    product_id = random.choice(PRODUCT_ID)
    container_id = fake.iban()
    
    for pos in PO_NUMBER:
        a = open('./outputs/ASN.json')
        asn_data = json.load(a)
        for j in asn_data:
            if pos == j["PONumber"]:
                ASN.append(j["ASNNumber"])
        asn_number = random.choice(ASN)
        asn_line = random.randint(1000, 999999)

        f = open('./outputs/POLine.json')
        json_data = json.load(f)
        for i in json_data:
            if pos == i["PONumber"]:
                po_line = (i["POLine"])
                order_quantity = i["OrderQuantity"]
                container_position = random.choice(["In-Transit", "Docked", "Loading", "Empty", "Delivered"])
                promised_quantity = order_quantity - random.randint(1, 8)
                delivered_quantity = promised_quantity - random.randint(1, 5)
                
                gross_amount = round(float(''.join([random.choice('123456789') for _ in range(2)])) * 1.1, 2)
                tax_amount = int(gross_amount) * int(''.join([random.choice('12') for _ in range(1)])) / 10
                discount_amount = round((gross_amount + tax_amount) * int(''.join([random.choice('123') for _ in range(1)])) / 10,
                                        2)
                net_amount = round((gross_amount + tax_amount) - discount_amount, 2)

                create_date = utils.get_create_date().isoformat()
                update_date = fake.past_datetime().isoformat()

                output = {
                    "ASNNumber": asn_number,
                    "ASNLine": asn_line,
                    "ProductId": product_id,
                    "ContainerId": container_id,
                    "ContainerPosition": container_position,
                    "PONumber": pos,
                    "POLine": po_line,
                    "OrderQty": order_quantity,
                    "PromiseQty": promised_quantity,
                    "ShippedQty": delivered_quantity,
                    "GrossAmount": gross_amount,
                    "TaxAmount": tax_amount,
                    "DiscountAmount": discount_amount,
                    "NetAmount": net_amount,
                    "CreateDate": create_date,
                    "UpdateDate": update_date,
                    "UpdateCount": 0
                }

                FINAL.append(output)

    return FINAL

# def data_generator(count):
#     global TEMP_ASN_ID, TEMP_PRODUCT_ID, TEMP_PO_NUMBER
#     data = []

#     TEMP_ASN_ID = asn_ids.copy()
#     TEMP_PRODUCT_ID = product_ids.copy()
#     TEMP_PO_NUMBER = po_ids.copy()

#     # Generate data
#     for _ in range(count):
#         output = asn_line_data(po_ids)
#         data.append(output)

#     return data