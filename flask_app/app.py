import os
from flask import Flask, redirect, url_for, session, request, jsonify
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

app = Flask(__name__)

# OAuth 2.0 client configuration
GOOGLE_CLIENT_SECRETS_FILE = "credentials.json"  # Path to your credentials file
API_SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# Secret key for session management
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "your_secret_key")  # Replace with your own secret key

# Route to start the authorization process
@app.route("/authorize")
def authorize():
    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_FILE,
        scopes=API_SCOPES,
        redirect_uri=url_for("callback", _external=True)
    )
    authorization_url, state = flow.authorization_url(access_type="offline", include_granted_scopes="true")
    session["state"] = state  # Save the state to verify in the callback
    return redirect(authorization_url)

# Callback route to handle the OAuth2 authorization response
@app.route("/callback")
def callback():
    # Retrieve the state from the session
    state = session["state"]

    # Create a flow object to fetch the token
    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_FILE,
        scopes=API_SCOPES,
        state=state,
        redirect_uri=url_for("callback", _external=True)
    )

    # Fetch the token after the user grants authorization
    flow.fetch_token(authorization_response=request.url)

    # Store the credentials in the session
    credentials = flow.credentials
    session["credentials"] = credentials_to_dict(credentials)

    # Redirect to access the Google Sheets data
    return redirect(url_for('access_google_sheets'))

# Route to access Google Sheets and fetch data
@app.route("/access_google_sheets")
def access_google_sheets():
    credentials = session.get("credentials")
    if not credentials:
        return redirect(url_for("authorize"))  # Redirect to login if no credentials are available

    # Build the Google Sheets API service object
    creds = Credentials.from_authorized_user_info(info=credentials)
    service = build("sheets", "v4", credentials=creds)

    # Specify the spreadsheet ID and range (adjust as needed)
    spreadsheet_id = "your_spreadsheet_id_here"  # Replace with your actual spreadsheet ID
    range_name = "Sheet1!A1:D10"  # Adjust the range based on your data
    sheet = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()

    # Fetch the data and return it as a JSON response
    values = sheet.get("values", [])
    return jsonify(values)

# Function to convert credentials to a dictionary
def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }

# Route to create and process a report (example)
@app.route("/create_report", methods=["POST"])
def create_report():
    data = request.json
    patient_data = get_patient_data(data["patient_id"])  # Define this function based on your needs

    decision = process_data(patient_data, data["inputs"])  # Define this function to process patient data
    updated_report = update_report_with_llm(decision)  # Define this function for LLM output

    # Create report and send to target URL (e.g., Make or Camunda)
    report = {
        "patient_id": data["patient_id"],
        "decision": decision,
        "llm_output": updated_report
    }

    target_url = data.get("target_url")  # Webhook URL or Camunda endpoint
    send_status = send_report(report, target_url)  # Define this function to send the report
    
    return jsonify({"report": report, "send_status": send_status})

# Placeholder function for getting patient data (you can define it based on your database)
#def get_patient_data(patient_id):
    # Example: Fetch patient data from a database or external service
 #   return {"name": "John Doe", "age": 45}

# Placeholder function for processing patient data (you can implement the actual logic)
#def process_data(patient_data, inputs):
    # Example: Make decisions based on patient data and inputs
 #   return f"Processed data for {patient_data['name']}"

# Placeholder function for updating the report with LLM (define the actual logic)
#def update_report_with_llm(decision):
    # Example: Update the report with LLM-generated content
 #   return f"LLM Output for decision: {decision}"

# Placeholder function to send the report (implement based on your target service, e.g., Make or Camunda)
#def send_report(report, target_url):
    # Example: Send the report to a target URL
 #   return {"status": "success", "url": target_url}

if __name__ == "__main__":
    # Running the Flask app (use app.run() for development or 'serve' for production)
    app.run(debug=True, host="0.0.0.0", port=8000)