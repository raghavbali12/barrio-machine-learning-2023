import urllib.request
import json
import os
import ssl
import ClassSession
import csv
import config  # import the config module

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Open and read the csv and parse its contents
with open('Barrio Class Data 2023 - Machine Learning Data.csv', newline='') as csvFile:
    reader = csv.reader(csvFile, delimiter=',', quotechar='|')
    for row in reader:
        print(row)

# Request data goes here
# The example below assumes JSON formatting which may be updated
# depending on the format your endpoint expects.
# More information can be found here:
# https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
data =  {
  "input_data": {
    "columns": [
      "Session Start Time",
      "Class",
      "Instructor",
      "Time",
      "Day of the Week",
      "Season",
      "Date",
      "Class Type",
      "Level"
    ],
    "index": [0],
    "data": [
    ]
  }
}

body = str.encode(json.dumps(data))

url = 'https://barriodanceml-jebdj.centralus.inference.ml.azure.com/score'
# Replace this with the primary/secondary key or AMLToken for the endpoint
api_key = config.api_key  # use the api_key from config
if not api_key:
    raise Exception("A key should be provided to invoke the endpoint")

# The azureml-model-deployment header will force the request to go to a specific deployment.
# Remove this header to have the request observe the endpoint traffic rules
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'barriodance2023classes-1' }

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    print(result)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(error.read().decode("utf8", 'ignore'))
