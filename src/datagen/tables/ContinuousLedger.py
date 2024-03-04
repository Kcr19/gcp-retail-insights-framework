from faker import Faker
import datetime as dt
from datetime import timedelta as td

import json
import utils
import random
import math

# Instantiate Faker
fake = Faker()
NODE_ID = []
PRODUCTS = {}
INVENTORY = {}
FORECAST = {}

def data_generator(count, ids):
    global TEMP_PRODUCT_ID
    data = []

    f = open('./outputs/RefNode.json')
    json_data = json.load(f)
    for i in json_data:
        if i['NodeId'].startswith('DC'):
            NODE_ID.append(i['NodeId'])
    
    f = open('./outputs/RefProduct.json')
    json_data = json.load(f)
    for i in json_data:
        pr = {}
        pr['DefaultSellingPrice'] = i['DefaultSellingPrice']
        pr['Class'] = i['Class']
        pr['ShelfLifeDays'] = i['ShelfLifeDays']
        PRODUCTS[i['ProductId']] = pr


    TEMP_PRODUCT_ID = ids.copy()

    f = open('./outputs/RefInventory.json')
    json_data = json.load(f)
    for i in json_data:
        inv = {}
        inv['MfgDate'] = i['MfgDate']
        inv['ProductId'] = i['ProductId']
        inv['Quantity'] = i['Quantity']
        inv['LocationNode'] = i['LocationNode']
        INVENTORY[i['InventoryId']] = inv

    f = open('./outputs/RefForecast.json')
    json_data = json.load(f)
    for i in json_data:
        fcst = {}
        fcst['DemandDate'] = i['DemandDate']
        fcst['LocationNode'] = i['LocationNode']
        fcst['ProductId'] = i['ProductId']
        fcst['Quantity'] = i['Quantity']
        FORECAST[i['ForecastId']] = fcst

    iter_month = 1
    today = dt.date.today()
    start_date = dt.date(2022,1,1)
    iter_year = start_date.year
    end_date = today+td(days=365*4)
    ledger = [{} for i in range((end_date.year-start_date.year)*12+end_date.month-start_date.month)]

    for inv_k in INVENTORY.keys():
        mfg_date = dt.datetime.fromisoformat(INVENTORY[inv_k]['MfgDate'])
        exp_date = mfg_date+td(days=PRODUCTS[INVENTORY[inv_k]['ProductId']]['ShelfLifeDays'])
        exp_month = dt.date(exp_date.year, exp_date.month, 1)
        product_id = INVENTORY[inv_k]['ProductId']
        loc = INVENTORY[inv_k]['LocationNode']

        ledger_idx = (exp_month.year-2022)*12+exp_month.month

        if loc not in ledger[ledger_idx]:
            ledger[ledger_idx][loc] = {}
        if product_id not in ledger[ledger_idx][loc]:
            ledger[ledger_idx][loc][product_id] = {'Inv_Quantity': 0, 'Fcst_Quantity':0}

        entry = ledger[ledger_idx][loc][product_id]
        entry['Inv_Quantity'] += INVENTORY[inv_k]['Quantity']

    for fcst_k in FORECAST.keys():
        forecast_date = dt.datetime.fromisoformat(FORECAST[fcst_k]['DemandDate'])
        fcst_month = dt.date(forecast_date.year, forecast_date.month, 1)
        ledger_idx = (fcst_month.year-2022)*12+fcst_month.month
        product_id = FORECAST[fcst_k]['ProductId']
        loc = FORECAST[fcst_k]['LocationNode']

        if loc not in ledger[ledger_idx]:
            ledger[ledger_idx][loc] = {}
        if product_id not in ledger[ledger_idx][loc]:
            ledger[ledger_idx][loc][product_id] = {'Inv_Quantity': 0}
            ledger[ledger_idx][loc][product_id] = {'Fcst_Quantity': 0}
        if 'Fcst_Quantity' not in ledger[ledger_idx][loc][product_id]:
            ledger[ledger_idx][loc][product_id] = {'Fcst_Quantity': 0}

        entry = ledger[ledger_idx][loc][product_id]
        entry['Fcst_Quantity'] += FORECAST[fcst_k]['Quantity']
        

    data = []
    curr_qtys = {}

    for idx in range(len(ledger)):
        for loc in ledger[idx]:
            for product_id in ledger[idx][loc]:
                for fut_idx in range(idx,min(idx+6,len(ledger))):
                    scrap_count = 0
                    if loc in ledger[fut_idx] and product_id in ledger[fut_idx][loc] and 'Inv_Quantity' in ledger[fut_idx][loc][product_id]:
                        scrap_count += ledger[fut_idx][loc][product_id]['Inv_Quantity']

                prd = PRODUCTS[product_id]

                if product_id not in curr_qtys:
                    curr_qtys[product_id] = 0

                qty_dict = ledger[idx][loc][product_id]

                if 'Inv_Quantity' in qty_dict:
                    curr_qtys[product_id] += qty_dict['Inv_Quantity']
                    
                record = {
                    "DistributionCenterId": loc,
                    "ProductId": product_id,
                    "Category": prd['Class'],
                    #"Batch": ??,
                    "ExpiryDate": dt.date(2022+math.floor((idx-1)/12), ((idx-1)%12)+1, 1).isoformat(),
                    "DemandAmt":  int(prd['DefaultSellingPrice']*qty_dict['Fcst_Quantity']),
                    "DemandUnits": int(qty_dict['Fcst_Quantity']),
                    #"ProjectionDate": ??,
                    "InventoryOnHandAmount": int(curr_qtys[product_id]*prd['DefaultSellingPrice']),
                    "InventoryOnHandUnits": int(curr_qtys[product_id]),
                    "EOMInventoryAmount": int((curr_qtys[product_id]-qty_dict['Fcst_Quantity'])*prd['DefaultSellingPrice']),
                    "EOMInventoryUnits": int(curr_qtys[product_id]-qty_dict['Fcst_Quantity']),
                    "ScrapInventoryUnits": int(scrap_count),
                    "ScrapInventoryAmount": int(scrap_count*prd['DefaultSellingPrice']),
                }

                curr_qtys[product_id] -= qty_dict['Fcst_Quantity']
                data.append(record)

    return data
