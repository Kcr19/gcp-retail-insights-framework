#Copyright 2023 Google LLC
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#https://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

import os
import sys
import json
import time
import subprocess

from os import system
from subprocess import Popen
from google.cloud import bigquery


def get_project_id():
    # Get user's GCP project information
    adc_gcloud = "gcloud info --format=json"
    get_adc_data = subprocess.check_output(adc_gcloud, shell=True).decode(sys.stdout.encoding)
    project_data = json.loads(get_adc_data)
    project_id = project_data['config']['project']
    return project_id


# Execute Terraform script
def build_infrastructure():
    # Terraform command step up
    terraform_cli_variables = ' -var "project=' + get_project_id() + '" '
    terraform_command_step1 = 'terraform init -upgrade'
    terraform_command_step2 = 'terraform apply -auto-approve -refresh=false' + terraform_cli_variables
    terraform_command_step3 = 'terraform output -json > ./infrastructure.json'

    # Switch to terraform script's directory
    os.chdir('./src/iac')

    # Execute terraform commands in order
    commands = [terraform_command_step1, terraform_command_step2, terraform_command_step3]
    for cmd in commands:
        subprocess.call(cmd, shell=True)

    os.chdir("../../")


# Generate fake data
def generate_data():
    # Generate sample data
    print("Generate sample data", os.getcwd())
    os.chdir('./src/datagen')
    process = Popen("python3 main.py", shell=True)
    process.wait()
    time.sleep(60)
    os.chdir('../')
    process.kill()


# Load data to GCS folder
def load_to_gcs(bukcet_name, output_folder):
    gcs_bucket_name = get_project_id() + bukcet_name
    dir_list = os.listdir(output_folder)
    for file in dir_list:
        process = Popen("gcloud storage cp " + output_folder + "/" + file + " gs://" + gcs_bucket_name + "", shell=True)
    process.wait()
    process.kill()


# Process data to load to BQ
def process_data():
    print("Data prep started")
    get_path = "./outputs"
    os.chdir("./datagen/outputs")
    dir_files = os.listdir()
    os.mkdir("clean")
    for file in dir_files:
        system("cat " + file + " | jq -c '.[]' > ./clean/" + file + " ")
    os.chdir("../../")
    load_to_gcs(bukcet_name="_retail_if_sample/", output_folder="./datagen/outputs/clean")


# Create Clustering
def create_bq_clustering():
    os.chdir("./datagen/tables")
    f = open('clustering.json')
    print('Creating Clustering')
    clustering_data = json.load(f)
    for i in clustering_data:
        process = Popen("bq update --clustering_fields="+i['keys']+" retail_dataset."+i['table_name']+" ", shell=True)
        process.wait()
    os.chdir("../../")


# Load data to Big Query
def bq_loader():
    print("Load data to BigQuery")
    client = bigquery.Client()
    project_id = get_project_id()
    table_id = project_id+".retail_dataset."
    job_config = bigquery.LoadJobConfig(autodetect=True, source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON)
    os.chdir("iac/table_schemas")
    dir_files = os.listdir()
    for file in dir_files:
        uri = "gs://"+project_id+"_retail_if_sample/"+file
        load_job = client.load_table_from_uri(uri, table_id+file.replace(".json", ""), job_config=job_config)
        load_job.result()
    print("Job ran successfully!")


# Create views
def create_view():
    print("Creating Views")
    client = bigquery.Client()
   
    # Get project id
    project_id = get_project_id()
    table_id = project_id+".retail_dataset."
    
    # Create view Id
    view_id = table_id+"rcim_po_visibility"
    view = bigquery.Table(view_id)
    
    view_sql = f"""SELECT po.PONumber AS po_num,
    po.POType AS po_type,
    po.OrderDate AS po_order_dt,
    po.NetAmount AS po_order_amt,
    po.CreateDate AS po_create_dt,
    po_status.UpdateDate AS po_upd_dt,
    po_status.POLine AS po_upd_po_line,
    COALESCE(po_status.Status,'N/A') AS po_upd_status,
    COALESCE(po_line.ProductId,'N/A') AS po_line_prod_id,
    COALESCE(po_line.ShipToNode,0) AS po_line_ship_to_node,
    COALESCE(po_line.OrderQuantity,0) AS po_line_order_qty,
    COALESCE(asn.ASNNumber,'N/A') AS asn_num,
    COALESCE(asn_line.POLine,0) AS asn_po_line,
    COALESCE(asn_line.PromiseQty,0) AS asn_promise_qty,
    COALESCE(asn_line.ShippedQty,0) AS asn_shipped_qty,
    COALESCE(ref_node.NodeId,'N/A') AS ref_node_id,
    COALESCE(ref_node.Type,'N/A') AS ref_node_type
    FROM
    `{table_id}PO` po
    LEFT JOIN `{table_id}POStatusUpdates` po_status
    ON po.PONumber = po_status.PONumber
    LEFT JOIN `{table_id}POLine` po_line
    ON po.PONumber = po_line.PONumber
    LEFT JOIN `{table_id}ASN` asn
    ON po.PONumber = asn.PONumber
    LEFT JOIN `{table_id}ASNLine` asn_line
    ON po.PONumber = asn_line.PONumber
    LEFT JOIN `{table_id}RefNode` ref_node
    ON po.ShipToNode = ref_node.NodeId"""

    # Create view
    view.view_query = view_sql

    # Make an API request to create the view.
    view = client.create_table(view)
    print(f"Created {view.table_type}: {str(view.reference)}")


def run():
    build_infrastructure()
    generate_data()
    process_data()
    create_bq_clustering()
    bq_loader()
    create_view()


if __name__ == "__main__":
    run()
