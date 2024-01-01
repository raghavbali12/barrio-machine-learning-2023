import urllib.request
import json
import os
import ssl
import ClassSession
import csv
import pandas as pd
import config # config.py
import os
import ssl
import pandas as pd
import config # config.py
import gspread
import gspread_dataframe as gd
from oauth2client.service_account import ServiceAccountCredentials

def allowSelfSignedHttps(allowed):
  # bypass the server certificate verification on client side
  if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
    ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Open and read the csv and parse its contents into a pandas dataframe
csvUrl = config.csvUrl
df = pd.read_csv(csvUrl)
wrapper = ClassSession.ClassSessionWrapper(df)

# Iterate over each row in the dataframe and send it to the endpoint
for index, row in df.iterrows():
  # Request data goes here
  # The example below assumes JSON formatting which may be updated
  # depending on the format your endpoint expects.
  # More information can be found here:
  # https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
  data =  {
    "input_data": {
      "columns": wrapper.get_columns(),
      "index": [index],
      "data": [wrapper.get_row(index).tolist()]
    }
  }

  body = str.encode(json.dumps(data))

  url = config.mlEndpointUrl
  # Replace this with the primary/secondary key or AMLToken for the endpoint
  api_key = config.api_key
  if not api_key:
      raise Exception("A key should be provided to invoke the endpoint")

  # The azureml-model-deployment header will force the request to go to a specific deployment.
  # Remove this header to have the request observe the endpoint traffic rules
  headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'barriodance2023classesv2-1' }

  req = urllib.request.Request(url, body, headers)

  try:
    response = urllib.request.urlopen(req)

    result = response.read()
    output_str = result.decode('utf-8')  # Decode from bytes to string
    output_num = round(float(output_str.strip('[]')), 1)  # Remove brackets and convert to float 
    df.loc[index, 'Predicted Number of Students'] = output_num

    # Write the updated dataframe to google sheets
    scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('barriodance2023ml-0ef76a5777c6.json', scope)

    gc = gspread.authorize(credentials)

    # Open the Google Spreadsheet
    spreadsheet = gc.open('Barrio Class Data 2023')

    # Select a worksheet from the spreadsheet
    worksheet = spreadsheet.worksheet('Machine Learning Predictions 2024')

    # Write the DataFrame to the worksheet
    gd.set_with_dataframe(worksheet, df)

  except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(error.read().decode("utf8", 'ignore'))
