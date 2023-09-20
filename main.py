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


def run():
    build_infrastructure()
    generate_data()
    process_data()
    bq_loader()


if __name__ == "__main__":
    run()