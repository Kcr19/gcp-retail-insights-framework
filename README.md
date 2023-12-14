# Retail Insights Canonical Framework for Supply Chain
## Why Retail Insights Framework?
The need for a retail insights framework is driven by the increasing complexity of retail businesses. As retailers expand their product offerings, open new stores, and enter new markets, they need to be able to manage and analyze large amounts of data in order to make informed business decisions. A framework to derive these insights can help retailers to consolidate and standardize their data, making it easier to access and analyze.
An insight framework can also help to improve the efficiency of retail operations. By providing a common understanding of the data, the framework can help to break down data silos and improve communication between different departments within a retail business. This can lead to improved decision-making, reduced costs, and increased profits.

## Solution Approach
The framework will initially focus on the PO visibility based on PO status updates. The goal is to position the framework as as an accelerator with the following components:
Reference architecture and data model
Pre-built automation scripts to create the data model and populate it with synthetic data. This script can be easily deployed by customers or partners in a Google Cloud project
Looker Studio dashboards focusing on common use cases

## Prerequisites
### Software requirements
If you are running the RetailModel Package in

**Local machine** \
Download Terraform \
Run ```terraform --version ``` to check if terraform is installed \
Download Python Version 3 \
Run ```python3 --version ``` to check the version of Python

**Cloud Shell** \
None

### Authentication & Project Setup \
The Retail Model uses ADC to build the required GCP infrastructure.
This step is needed only if your running Retail Model from your local machine
Open command prompt. To create your credentials file run the following command - \
``gcloud auth application-default login ``\
Optional: To list all the project properties, run: \
``gcloud config list --all`` \
To ensure you are doing this in the correct project be sure to check and/or set it. \
``gcloud config set project [PROJECT_ID] ``

### Permissions \
Permissions needed (for the id you are running this with)\
``roles/bigquery.dataEditor``
``roles/storage.admin``

### Download Retail Model
Clone Retail Model repo. \
``git clone https://github.com/Kcr19/gcp-retail-insights-framework``

### Deploy Retail Model in your project \
cd into the RetailModel folder [Time: 5 mins]\
``python3 main.py``

### Deleting Retail Model Infrastructure (optional) \
If for any reason, data is missing or if you would like to delete the Google Cloud resources created, run the below code in your terminal.  Reference
cd into src/iac to run terraform destroy \
``terraform destroy -var "project=<your-project-name>"``

### Creating the Looker Studio report

This <a href ="https://lookerstudio.google.com/u/0/reporting/f42c2d7f-a15d-4cc6-a8e7-0fa90685dbf0/page/p_k5114r9s9c" target="_blank">sample report </a> uses a synthetic supply chain dataset to display purchase order (PO) information by PO Status along with PO Line and Advanced Shipping Notice (ASN) details. The report can be filtered by a specific Shipping Node, PO Type and date range.

To use your own data for this report, follow these steps:
1) Make a <a href ="https://support.google.com/looker-studio/answer/7175478?hl=en#zippy=%2Cin-this-article" target="_blank">copy </a>of this report
2) In your copied report, click the Edit button to go into Edit mode on the report
3) In the Data pane, hover over the BigQuery icon and click the "Edit data source" icon.
4) In the data editing screen that appears, click Edit Connection
5) Select your BigQuery billing project, dataset and table/view where your data is stored.

* Additional details on editing a Looker Studio data source can be found <a href ="https://support.google.com/looker-studio/answer/7178497?hl=en#zippy=%2Cin-this-article" target="_blank">here </a>.

* Note that your data source schema must match the schema of the sample data. Use the code repository referenced above to generate the source schema and synthetic data.
