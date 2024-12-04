from flask import Flask, render_template
import googleapiclient.discovery
from google.oauth2 import service_account
import json

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

    # Render the data in your template
    return render_template("index.html", values=values)

# decision making in decisions.py to keep the app lean


def check_patient_status(patients, surgery_data, bending_angle, pain)



if __name__ == '__main__':
    app.run(debug=True)