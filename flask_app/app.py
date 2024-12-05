from flask import Flask, render_template
import googleapiclient.discovery
from google.oauth2 import service_account
import json
#from utils.LLM_utils import generate_report
from flask import jsonify

app = Flask(__name__)

# Load configuration from JSON file
with open("config.json") as config_file:
    config = json.load(config_file)

# Make sure the credentials are loaded after config is available
def get_credentials():
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    GOOGLE_PRIVATE_KEY = config.get('private_key')
    GOOGLE_CLIENT_EMAIL = config.get('client_email')

    account_info = {
        "private_key": GOOGLE_PRIVATE_KEY,
        "client_email": GOOGLE_CLIENT_EMAIL,
        "token_uri": "https://accounts.google.com/o/oauth2/token",
    }
    
    credentials = service_account.Credentials.from_service_account_info(account_info, scopes=scopes)
    return credentials

def get_service(service_name="sheets", api_version="v4"):
    credentials = get_credentials()
    service = googleapiclient.discovery.build(service_name, api_version, credentials=credentials)
    return service

@app.route("/")
def home():
    return "The app is running"

@app.route("/patient_data", methods=["GET"])
def homepage():
    service = get_service()
    
    # Ensure you extract the correct spreadsheet ID from the config file
    spreadsheet_id = config.get("spreadsheet_id")  # Retrieve the spreadsheet ID from config.json
    range_name = "Sheet1"  # Retrieve the entire Sheet1

    # Get the entire content of Sheet1
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    
    # Extract values from the result
    values = result.get("values", [])

    # Return the data as JSON
    return jsonify(values)


#@app.route("/generate_report/<int:patient_id>", methods=["GET"])
#def generate_patient_report(patient_id):
   # service = get_service()
    #spreadsheet_id = config.get("spr
    #eadsheet_id")
    #range_name = "Sheet1"  # Define the range for your data

    # Fetch patient data from Google Sheets
    #result = service.spreadsheets().values().get(
    #    spreadsheetId=spreadsheet_id, range=range_name).execute()
   # values = result.get("values", [])

    # Ensure patient ID is valid
    #if patient_id < 0 or patient_id >= len(values):
     #   return {"error": "Invalid patient ID"}, 400

    # Map the row to patient data
    #header = values[0]  # Assumes the first row contains column names
    #patient_row = values[patient_id + 1]  # Patient data starts from the second row
    #patient_data = dict(zip(header, patient_row))

    # Generate the report
  #  report = generate_report(patient_data)
    
    # Return the report
   # return {"report": report}


if __name__ == '__main__':
    app.run(debug=True)