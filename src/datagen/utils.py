import os
import json
import random

from faker import Faker
from datetime import date

from tables import PO
from tables import ASN
from tables import PII
from tables import Node
from tables import Task
from tables import Trade
from tables import Orders
from tables import Layout
from tables import POLine
from tables import ASNLine
from tables import Product
from tables import Customer
from tables import POStatus
from tables import Associate
from tables import OrderLine
from tables import ProductPrice
from tables import Replenishment
from datetime import datetime as dt
from datetime import timedelta as td

fake = Faker()

NO_OF_RECORDS = 1000

PII_TOKEN = list(str(fake.isbn10()) for _ in range(NO_OF_RECORDS))
ORDER_ID = list("order-" + str(fake.unique.ean(length=8)) for _ in range(NO_OF_RECORDS))
ASSOCIATE_ID = list("associate-" + str(fake.unique.ean(length=8)) for _ in range(NO_OF_RECORDS))
TRADE_PARTNER_ID = list("trade-" + str(fake.unique.ean(length=8)) for _ in range(NO_OF_RECORDS))
NODE_ID = list(str(fake.unique.ean(length=8)) for _ in range(int(NO_OF_RECORDS)))
LAYOUT_ID = list(str(fake.iban()) for _ in range(NO_OF_RECORDS))
LOYALTY_ID = list(str(fake.iban()) for _ in range(NO_OF_RECORDS))
PRODUCT_ID = list(str(fake.pystr()) for _ in range(NO_OF_RECORDS))
CUSTOMER_ID = list(fake.iban() for _ in range(NO_OF_RECORDS))
PO_NUMBER = list("po-" + str(fake.unique.ean(length=8)) for _ in range(int(NO_OF_RECORDS / 10)))
ASN_ID = list("asn-" + str(fake.iban()) for _ in range(NO_OF_RECORDS))
PO_LINE_NUMBER = list(''.join([random.choice('0123456789') for _ in range(13)]) for _ in range(NO_OF_RECORDS))


def get_create_date():
    create_date = dt.now() - \
                  td(days=random.randint(1, 365),
                     hours=random.randint(1, 24),
                     minutes=random.randint(1, 60),
                     seconds=random.randint(1, 60)
                     )
    return create_date


def get_year():
    start = date(2010, 1, 1)
    end = date(2020, 1, 1)
    year_range = [year for year in range(start.year, end.year + 1)]
    year = random.choice(year_range)
    return year


def create_json(data, table_name):
    """
    Creates a json like output and stores in a folder
    :return: None
    """

    if table_name != "POStatusUpdates":
        convert_to_json = json.dumps(data)
    else:
        convert_to_str = ''.join(str(data)).replace('"', '').replace("'", '"')
        convert_to_json = convert_to_str
    
    # Store the json output to outputs folder
    with open(os.getcwd() + '/outputs/' + table_name + '.json', "w+") as outfile:
        outfile.write(convert_to_json)


def make_output_folder():
    current_path = os.getcwd()
    make_folder = os.path.join(current_path, "outputs")
    os.mkdir(make_folder)
    print('Data folder created')


def generate_data():
    # Generate data
    print("Data Generation started")
    create_json(data=PII.data_generator(count=NO_OF_RECORDS, ids=PII_TOKEN), table_name="PII")
    create_json(data=Task.data_generator(count=NO_OF_RECORDS), table_name="RefTask")
    create_json(data=Product.data_generator(count=NO_OF_RECORDS, ids=PRODUCT_ID), table_name="RefProduct")
    create_json(data=Layout.data_generator(count=NO_OF_RECORDS, ids=LAYOUT_ID), table_name="NodeLayout")
    create_json(data=Customer.data_generator(count=NO_OF_RECORDS, node_ids=CUSTOMER_ID,
                                             loyalty_ids=LOYALTY_ID), table_name="RefCustomer")
    create_json(data=Associate.data_generator(count=NO_OF_RECORDS, ids=ASSOCIATE_ID),
                table_name="RefAssociate")
    create_json(data=Node.data_generator(count=NO_OF_RECORDS, ids=NODE_ID), table_name="RefNode")
    create_json(data=Trade.data_generator(count=NO_OF_RECORDS, ids=TRADE_PARTNER_ID),
                table_name="RefTradePartner")
    create_json(data=Replenishment.data_generator(count=NO_OF_RECORDS, ids=PRODUCT_ID),
                table_name="RefReplenishment")
    create_json(
        data=Orders.data_generator(count=NO_OF_RECORDS, order_ids=ORDER_ID, customer_ids=CUSTOMER_ID,
                                   associate_ids=ASSOCIATE_ID), table_name="SalesOrder")
    create_json(
        data=OrderLine.data_generator(count=NO_OF_RECORDS, order_ids=ORDER_ID,
                                      product_ids=CUSTOMER_ID), table_name="SalesOrderLine")
    create_json(data=ProductPrice.data_generator(count=NO_OF_RECORDS), table_name="RefProductPrice")
    create_json(data=PO.data_generator(count=int(NO_OF_RECORDS / 10), ids=PO_NUMBER), table_name="PO")
    create_json(
        data=POLine.data_generator(count=NO_OF_RECORDS, po_line_ids=PO_LINE_NUMBER,
                                   node_ids=NODE_ID, product_ids=PRODUCT_ID), table_name="POLine")
    create_json(data=ASN.data_generator(count=NO_OF_RECORDS, asn_ids=ASN_ID, po_ids=PO_NUMBER,
                                        node_ids=NODE_ID,
                                        trade_ids=TRADE_PARTNER_ID), table_name="ASN")
    create_json(data=ASNLine.run(PO_NUMBER, PRODUCT_ID), table_name="ASNLine")
    create_json(data=POStatus.po_update_data(), table_name="POStatusUpdates")


    print("Data generation is complete")
