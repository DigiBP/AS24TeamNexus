import os
from flask import Flask, redirect, url_for, session, request, jsonify
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

app = Flask(__name__)

#OAuth 2.0 cluent configuration
GOOGLE_CLIENT_SECRETS_FILE = "credentials.json"
API_SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"] 

@app.route("/authorize")
def authorize():
    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_FILE,
        scopes=API_SCOPES,
        redirect_uri = url_for("callback", _external=True)
    )
    authorization_url, state = flow.authorization_url(access_type="offline", include_granted_scopes= "true")
    session["state"] = state  
    return redirect(authorization_url)

# Callback to receive the authorization code
@app.route("/callback")
def callback():
    state = session["state"]
   flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_FILE,
        scopes=API_SCOPES,
        state=state,
        redirect_uri=url_for('callback', _external=True)
    )

    # Fetch the token after authorization
    flow.fetch_token(authorization_response=request.url)

    # Store credentials in the session
    credentials = flow.credentials
    session["credentials"] = credentials_to_dict(credentials)

    return redirect(url_for('access_google_sheets'))

@app.route("/access_google_sheets")
def access_google_sheets():
     credentials = session.get("credentials")
    if not credentials:
        return redirect(url_for("authorize"))  # Redirect to login if no credentials are available

    # Build Google Sheets API service object
    creds = Credentials.from_authorized_user_info(info=credentials)
    service = build("sheets", "v4", credentials=creds)

    # Specify the spreadsheet ID and range
    spreadsheet_id = "patient_data"
    range_name = "Sheet1!A1:D10"  # Adjust the range based on data
    sheet = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()

    # Fetch data and return it as a JSON response
    values = sheet.get("values", [])
    return jsonify(values)

# create a report

@app.route("/create_report", methods=["POST"])
def create_report():
    data = request.json
    patient_data = get_patient_data(data["patient_id"])
    
    decision = process_data(patient_data, data["inputs"])
    updated_report = update_report_with_llm(decision)
    
    # create report and send to make or camunda
    report = {
        "patient_id": data["patient_id"],
        "decision": decision,
        "llm_output": updated_report
    }

    target_url = data.get("target_url") # webhook url or camunda endpoint
    send_status = send_report(report, target_url)
    
    return jsonify({"report": report, "send_status": send_status})

if __name__ == "__main__":
    #app.run(debug=True)
    serve(app, host='0.0.0.0', port=8000, threads=30)
