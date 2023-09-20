from faker import Faker

import json
import utils
import random

# Instantiate Faker
fake = Faker()

ASN = []
PO_LINE = []


def asn_line_data(po_ids):
    """
    Generates fake data for the ASN Line table
    :return: fake ASN Line data
    """
    print("ASNLine ======================= ")
    for pos in po_ids:
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
                output = {
                    "ASN": asn_number,
                    "ASNLine": asn_line,
                    "PO_NUMBER": pos,
                    "PO_LINE": po_line,
                    "Order Quantity": order_quantity
                }

                print("ASNLine", output)

                return output


def data_generator(count, asn_ids, product_ids, po_ids):
    global TEMP_ASN_ID, TEMP_PRODUCT_ID, TEMP_PO_NUMBER
    data = []

    TEMP_ASN_ID = asn_ids.copy()
    TEMP_PRODUCT_ID = product_ids.copy()
    TEMP_PO_NUMBER = po_ids.copy()

    # Generate data
    for _ in range(count):
        output = asn_line_data(po_ids)
        data.append(output)

    return data




########################

po_number = None

    # asn_number = random.choice(TEMP_ASN_ID)
    # asn_line = random.randint(1000, 999999)
    # po_line = random.choice(utils.PO_LINE_NUMBER)
    # product_id = random.choice(TEMP_PRODUCT_ID)
    # container_id = fake.iban()
    # container_position = random.choice(["In-Transit", "Docked", "Loading", "Empty", "Delivered"])

    # # Get Node metadata from node.json
    # f = open('./outputs/ASN.json')
    # json_data = json.load(f)
    # for i in json_data:
    #     if asn_number == i["ASNNumber"]:
    #         po_number = i["PONumber"]

    # p = open('./outputs/POLine.json')
    # po_line_data = json.load(p)
    # for j in po_line_data:
    #     if po_line == j["POLine"]:
    #         order_quantity = j["OrderQuantity"]
    #         promised_quantity = order_quantity - random.randint(1, 8)
    #         delivered_quantity = promised_quantity - random.randint(1, 5)
            
    #         gross_amount = round(float(''.join([random.choice('123456789') for _ in range(2)])) * 1.1, 2)
    #         tax_amount = int(gross_amount) * int(''.join([random.choice('12') for _ in range(1)])) / 10
    #         discount_amount = round((gross_amount + tax_amount) * int(''.join([random.choice('123') for _ in range(1)])) / 10,
    #                                 2)
    #         net_amount = round((gross_amount + tax_amount) - discount_amount, 2)

    #         create_date = utils.get_create_date().isoformat()
    #         update_date = fake.past_datetime().isoformat()


    #         output = {
    #             "ASNNumber": asn_number,
    #             "ASNLine": asn_line,
    #             "ProductId": product_id,
    #             "ContainerId": container_id,
    #             "ContainerPosition": container_position,
    #             "PONumber": po_number,
    #             "POLine": po_line,
    #             "OrderQty": order_quantity,
    #             "PromiseQty": promised_quantity,
    #             "ShippedQty": delivered_quantity,
    #             "GrossAmount": gross_amount,
    #             "TaxAmount": tax_amount,
    #             "DiscountAmount": discount_amount,
    #             "NetAmount": net_amount,
    #             "CreateDate": create_date,
    #             "UpdateDate": update_date,
    #             "UpdateCount": 0
    #         }

    #         return output
