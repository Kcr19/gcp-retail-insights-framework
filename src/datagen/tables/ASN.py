from faker import Faker

import json
import utils
import random

# Instantiate Faker
fake = Faker()


def asn_data():
    """
    Generates fake data for the ASN table
    :return: fake ASN data
    """

    asn_number = random.choice(TEMP_ASN_ID)
    # if asn_number in TEMP_ASN_ID:
    #     TEMP_ASN_ID.remove(str(asn_number))

    asn_date = utils.get_create_date().isoformat()
    po_number = random.choice(TEMP_PO_NUMBER_ID)
    ship_date = utils.get_create_date().isoformat()
    carrier_id = random.choice(TEMP_TRADE_ID)
    transport_mode = random.choice(["Road", "Rail", "Ocean", "Air"])
    transport_id = "trns-id"+''.join([random.choice('0123456789') for _ in range(6)])
    transport_route = "trns-rt"+''.join([random.choice('0123456789') for _ in range(8)])
    transport_stop_id = "trns-stp"+''.join([random.choice('0123456789') for _ in range(10)])
    destination_node = random.choice(TEMP_NODE_ID)
    bol_number = "bol-"+''.join([random.choice('0123456789') for _ in range(13)])
    cert_origin = fake.country()
    customs_decl = fake.country()
    gross_amount = round(float(''.join([random.choice('123456789') for _ in range(2)])) * 1.1, 2)
    tax_amount = int(gross_amount) * int(''.join([random.choice('12') for _ in range(1)])) / 10
    discount_amount = round((gross_amount + tax_amount) * int(''.join([random.choice('123') for _ in range(1)])) / 10, 2)
    net_amount = round((gross_amount + tax_amount) - discount_amount, 2)
    create_date = utils.get_create_date().isoformat()
    update_date = fake.past_datetime().isoformat()

    output = {
        "ASNNumber": asn_number,
        "ASNDate": asn_date,
        "PONumber": po_number,
        "ShipDate": ship_date,
        "CarrierId": carrier_id,
        "TransportMode": transport_mode,
        "TransportId": transport_id,
        "TransportRouteId": transport_route,
        "TransportStopId": transport_stop_id,
        "DestinationNode": destination_node,
        "BOLNumber": bol_number,
        "CertOrigin": cert_origin,
        "CustomsDecl": customs_decl,
        "GrossAmount": gross_amount,
        "TaxAmount": tax_amount,
        "DiscountAmount": discount_amount,
        "NetAmount": net_amount,
        "CreateDate": create_date,
        "UpdateDate": update_date,
        "UpdateCount": 0
    }

    return output


def data_generator(count, asn_ids, po_ids, node_ids, trade_ids):
    global TEMP_ASN_ID, TEMP_PO_NUMBER_ID, TEMP_NODE_ID, TEMP_TRADE_ID
    data = []

    TEMP_ASN_ID = asn_ids.copy()
    TEMP_PO_NUMBER_ID = po_ids.copy()
    TEMP_NODE_ID = node_ids.copy()
    TEMP_TRADE_ID = trade_ids.copy()

    # Generate data
    for _ in range(count):
        output = asn_data()
        data.append(output)

    return data
