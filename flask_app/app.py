from flask import Flask, request, jsonify
from utils.google_sheets import get_patient_data
from utils.llm_utils import update_report_with_llm
from utils.decisions import process_data

app = Flask(__name__)

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
    app.run(debug=True)
