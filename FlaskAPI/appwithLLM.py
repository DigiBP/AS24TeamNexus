# LLM Part

import os
from haystack import Pipeline
from haystack.components.generators import HuggingFaceAPIGenerator
from haystack.components.builders.prompt_builder import PromptBuilder

# Ensure the Hugging Face API token is set in the environment
hf_token = os.environ.get("DIGIDBP")
if not hf_token:
    raise ValueError("DIGIDBP environment variable is not set!")

# Set the Hugging Face API token for the generator to use
os.environ["HF_API_TOKEN"] = hf_token

# Create the Hugging Face API generator
llm_generator = HuggingFaceAPIGenerator(
    api_type="serverless_inference_api",
    api_params={"model": "HuggingFaceH4/zephyr-7b-beta"}
)
# Define the text template
text_template = """
Role: Medical report generator. You must use only the information provided in the input data to generate the report. Do not include any details or assumptions that are not explicitly stated in the data.
**Medical Report: Post-Surgery Rehabilitation Transfer**

**Patient Information:**
- Name: {{ patient_firstname }} {{ patient_surname }}
- Date of Birth: {{ birthday }}
- Surgery Date: {{ surgery_date }}

**Prescribed Medications at discharge:**
- Paracetamol: {{ paracetamol }}
- Ibuprofen: {{ ibuprofen }}
- Pantoprazol: {{ pantoprazol }}
- Xarelto: {{ xarelto }}
- Oxycodon: {{ oxycodon }}
- Oxynorm: {{ oxynorm }}

**Rehabilitation Details:**
- Current Mobility: {{ mobility }}
- Secure Gait: {{ secure_gait }}

Ensure the generated text is concise and strictly limited to the above information.

Kind regards,  
Dr. med. Fredy Meier  
teamnexusdigibp@gmail.com
"""


# Initialize the pipeline with prompt builder and Hugging Face generator
pipe = Pipeline()

# Create the prompt builder
prompt_builder = PromptBuilder(template=text_template)

# Add components to the pipeline
pipe.add_component("prompt_builder", prompt_builder)
pipe.add_component("llm_generator", llm_generator)
pipe.connect("prompt_builder", "llm_generator")


def generate_medical_report(data):
    # Run the pipeline with the provided input

    relevant_inputs={
    "patient_surname": data.get("patient_surname","NA"),
    "patient_firstname": data.get("patient_firstname","NA"),
    "birthday": data.get("birthday","NA"),
    "surgery_date": data.get("surgery_date","NA"),
    "paracetamol": data.get("paracetamol","false"),
    "ibuprofen": data.get("ibuproven","false"),
    "pantoprazol": data.get("pantoprazol","false"),
    "xarelto": data.get("xarelto","false"),
    "oxycodon": data.get("oxycodon","false"),
    "oxynorm": data.get("oxynorm","false"),
    "mobility": data.get("mobility","walker")
    }

    medical_report_text = pipe.run(
        {
            "prompt_builder": relevant_inputs
        }
    )["llm_generator"]["replies"][0]
    # Print the generated report
    print(medical_report_text)
    return medical_report_text


#Sending the emails to the Healtcare facility, ATM it sends the report to our own email adress
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Implement the sending logic here
def send_medical_report(medical_report_text, email):
    # Gmail SMTP server configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "teamnexusdigibp@gmail.com"  
    sender_password = os.environ.get("GMAIL_APP_PASSWORD1")  

    if not sender_password:
        raise ValueError("GMAIL_APP_PASSWORD1 environment variable is not set!")

    try:
        # Create the email message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = email
        message["Subject"] = "Medical Report"

        # Attach the medical report text as the email body
        message.attach(MIMEText(medical_report_text, "plain"))

        # Connect to the Gmail server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Upgrade connection to secure TLS
            server.login(sender_email, sender_password)
            server.send_message(message)

        print(f"Email successfully sent to {email}!")

    except Exception as e:
        print(f"Failed to send email: {e}")


#API 
from flask import Flask, jsonify, request

app= Flask(__name__)
# Mocks the online Database of the Hospital
patients=[
  {
   "patient_id":1,"patient_surname":"jud",
   "patient_firstname":"domi",
   "birthday":"1.1.2000",
   "surgery_date":"1.1.2024",
   "email_address":"domi.jud@gmail.com"
   }, 
  {
    "patient_id": 2,
    "patient_surname": "Muster",
    "patient_firstname": "Kim",
    "birthday": "01-01-1999",
    "surgery_date": "02-05-2024",
    "email_address": "teamnexusdigibp@gmail.com"
  },
  {
    "patient_id": 3,
    "patient_surname": "Altesokke",
    "patient_firstname": "Tom",
    "birthday": "02-01-1999",
    "surgery_date": "01-07-2024",
    "email_address": "teamnexusdigibp@gmail.com"
  },
  {
    "patient_id": 4,
    "patient_surname": "Davidson",
    "patient_firstname": "Daniel",
    "birthday": "03-01-1999",
    "surgery_date": "08-06-2024",
    "email_address": "teamnexusdigibp@gmail.com"
  },
  {
    "patient_id": 5,
    "patient_surname": "Miller",
    "patient_firstname": "Elisa",
    "birthday": "04-01-1999",
    "surgery_date": "12-12-2024",
    "email_address": "elisa.hemmig@gmail.com"
  }
]
assessments=[{"patient_id":1, "patient_surname":"jud","patient_firstname":"domi","birthday":"1.1.2000","surgery_date":"1.1.2024","email_address":"domi.jud@gmail.com","paracetamol":True,"ibuprofen":True,"pantoprazol":True,"xarelto":True,"oxycodon":False,"oxynorm":False,"reha":False,"working":True,"homeoffice":True,"physio":False,"mobility":"walker","secure_gait":True}]
@app.route('/')
def welcome():
    return "Hello World"

@app.get('/api/patients')
def get_patients():
    return jsonify(patients)

@app.post('/api/patients')
def save_patient():
    data=request.get_json()
    patients.append(data)
    return "Ok"

@app.route('/api/patients/<id>', methods=["GET"])
def get_patient_by_id(id):
    for pat in patients:
        if pat["patient_id"]==int(id):
            return jsonify(pat)
    return jsonify({"error":"patient id not found"})



@app.get('/api/assessments')
def get_assessments():
    return jsonify(assessments)


@app.route('/api/assessments/<id>', methods=["GET"])
def get_assessment_by_id(id):
    for pat in assessments:
        if pat["patient_id"]==int(id):
            return jsonify(pat)
    return jsonify({"error":"patient id not found"})

@app.post('/api/assessments')
def save_assessment():
    data=request.get_json()
    print(data)
    assessments.append(data)
    return "Ok"

@app.post('/api/sendreport')
def send_report():
    data=request.get_json()
    report=generate_medical_report(data)
    send_medical_report(report,"teamnexusdigibp@gmail.com")
    return "OK"


@app.route('/api/latest', methods=["GET"])
def get_latest():
    return jsonify(assessments[-1])

if __name__=="__name__":
    app.run(host="0.0.0.0", port=8080)