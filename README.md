# Team Nexus 
### Patient Discharge Process after Total-Hip-Replacement Surgery

# Team members
Elisa Hemmig,
Justin Jouwena,
Dominique Jud,
Ramon Winkler

# Coaches
Andreas Martin,
Devid Montecchiari,
Charuta Pande

# Use-case Overview
Post-surgery care for total hip replacement (THR) patients is a highly complex and multi-disciplinary process that presents significant challenges for digitalization. In Switzerland, approximately 16,000 THR surgeries are performed annually, with each case followed by a recovery process involving daily assessments, discharge planning, and coordination among various stakeholders. The complexity of this process arises from the reliance on subjective judgment, real-time decision-making, and the interdependence of multiple roles.

During the hospital stay, patients undergo daily assessments that include monitoring the surgical wound, evaluating pain levels, and assessing mobility. Pain management relies on the Numerical Rating Scale (NRS), where patients self-report their pain on a scale from 1 to 10. This subjective data must be combined with the doctor’s clinical impressions to adjust medications effectively. Similarly, mobility evaluations involve physiotherapists and doctors assessing the patient’s ability to perform activities such as walking with a walker or climbing stairs. These assessments depend on subtle observations, such as detecting slight instability in gait or hesitancy in movement, which are challenging for digital systems to interpret.

Once the patient is deemed ready for discharge, they are either transferred to a rehabilitation center or sent home. For patients going to rehabilitation, only a summary of clinical findings is required, which is sent to the center to assume responsibility for ongoing care. However, for patients discharged home, several additional steps are required. The attending physician provides instructions to the Medical Assistant (MA), who prepares the necessary documents. These include a medication prescription adjusted to the patient’s needs, a physiotherapy referral specifying the patient’s mobility and gait at discharge, a certificate of incapacity to work tailored to the patient’s job, and a follow-up appointment scheduled for six weeks after surgery. The MA collaborates with the secretary to schedule the appointment, but conflicts with patient availability often arise, requiring rescheduling and revision of associated paperwork.

The patient is informed of their discharge plan, which includes details about their medication regimen, physiotherapy instructions, the follow-up appointment, and, if applicable, the certificate of incapacity to work. For patients going to a rehabilitation center, the process is simpler as the center takes over care management and requires fewer documents. In both cases, effective communication between the doctor, the MA, and the patient is critical to ensure a smooth transition.

Despite its structured nature, the discharge process is prone to bottlenecks. The MA may need to wait for the attending physician to finalize instructions, delaying the preparation of documents. Miscommunication between the MA and the secretary can result in scheduling errors for follow-up appointments, which require additional time to correct. Furthermore, the manual nature of the process, including the creation and handling of multiple documents, increases the risk of errors and inefficiencies.

Patients going home rely on detailed instructions to manage their recovery independently, while those transferred to rehabilitation rely on the center for further care. However, in both pathways, the process is heavily manual, time-consuming, and dependent on effective coordination among doctors, MAs, secretaries, and physiotherapists. These inefficiencies, coupled with the reliance on subjective assessments and fragmented workflows, underscore the need for digital optimization to streamline tasks, reduce delays, and improve the overall quality of care.

# As-Is Process

# Problems and Goals
**Fragmented Communication**
- Problem: The current process relies on manual handoffs between doctors, Medical Assistants (MAs), and secretaries, leading to delays and miscommunication.
- Why Digitalize: A centralized system ensures seamless data sharing and minimizes errors caused by fragmented workflows.

**Manual Document Preparation**
- Problem: The MA prepares multiple documents manually (medication prescription, physiotherapy referral, work incapacity certificate), which is time-consuming and prone to errors.
- Why Digitalize: Automated generation of these documents based on structured input would save time and ensure accuracy.

**Inefficient Follow-Up Appointment Scheduling**
- Problem: Appointments are scheduled manually by the resident and secretary, and rescheduling due to patient conflicts requires additional paperwork.
- Why Digitalize: A self-scheduling system allows patients to choose an appointment that fits their availability, reducing administrative burden.

**Rehabilitation Documentation Bottleneck**
- Problem: For patients going to rehabilitation, the summary report must be created manually, which can delay discharge if it is incomplete or incorrect.
- Why Digitalize: Automatically generating the rehabilitation report ensures faster and more accurate document preparation.

**Lack of Patient Empowerment**
- Problem: Patients rely on verbal or paper instructions, which can lead to confusion or lost information.
- Why Digitalize: Providing a digital link to access their documents and schedule appointments.

# To-Be Process
# Running The Process
# Make Scenarios
<img width="960" alt="make_scenario" src="https://github.com/user-attachments/assets/08747c41-f638-4faa-8474-dcb864be8323">

A Make Scenario was created as an external worker to generate and send customized medication prescriptions, physiotherapy prescriptions and medical certificates for each patient with a direct discharge from hospital to home. 

**Step 1: Connect to Camunda engine and define patient variables**
The Camunda engine notifies the scenario via webhook and a HTTP request module is used to fetch and lock the task. A Google sheet acts as patient database, where all patient information is saved. Each row corresponds to a patient and each column represents a variable. A filter is implemented to select for the latest patient entry by setting the bundle order position equal to the total number of bundles. A router module is added to create separate workflows, which are then activated by corresponding filters encoding the conditions for the patient variables. 

**Step 2: Send medication prescription (every patient)**
A customized medication prescription is generated for each patient. A medication list is created from the correspoding variables in the patient data base by a text aggregator module, which is inserted into a Google document that acts as template for the medication prescription. The customized medication prescription is saved on Google Drive and is retrieved by the file download module. The medication prescription is then sent to the patient email address along with a link, where the patient can schedule their first follow-up appointment. The last module of the branch is another HTTP request module notifying the Camunda engine about the completion of the external task. 

**Step 3a: Send physiotherapy prescription**
If a patient requires physiotherapy as per information in the patient data base, this branch is activated by means of a filter (physio = TRUE) and a customized physiotherapy prescription is prepared and sent to the patient by email. The instructions contain the generic reason for referral, an individualised status update on mobility and gait, as well as a generic follow-up plan. The customized document is created from a Google document template and saved on Google Drive (Module: "Create a document from a template"), and then retrieved (Module: "Download a file") and sent by email (Module: "Send an email") using the modules with the same functionalities as in step 2.

**Step 3b: Send medical certificate (general)**
If a patient works and no home office is possible, this branch is activated by means of a filter (working = TRUE, homeoffice = FALSE) and a general medical certificate is created for the employer and sent to the patient by email. It contains the duration of sick leave (6 weeks) and the preliminary return date, which is determined based on the surgery date. The same modules as in step 3a are used and configured appropriately. 

**Step 3c: Send medical certificate (home office)**
If a patient works and home office is possible, this branch is activated by means of a filter (working = TRUE, homeoffice = TRUE) and a medical certificate specifying the conditions for home office activities is created for the employer and sent to the patient by email. It contains the duration of sick leave (6 weeks) and the preliminary return date, which is determined based on the surgery date. The same modules as in step 3a are used and configured appropriately. 



# Flask API
Within a deepnote workspace a flask app was developed to store and return patient data. Deepnote is used to host the application. 
The application integrates a large language model (LLM) from Hugging Face ("HuggingFaceH4/zephyr-7b-beta") to generate detailed rehabilitation reports for patients. These reports are automatically sent to the rehabilitation team.

<table width="900">
    <tr>
        <th width="300"><b>Endpoint</b></th>
        <th width="50"><b>Method</b></th>
        <th width="250"><b>Description</b></th>
        <th width="100"><b>Request Body</b></th>
        <th width="200"><b>Response</b></th>
    </tr>
    <!-- Patient Endpoints -->
    <tr><td colspan="5"><b>Patient Endpoints</b></td></tr>
    <tr>
        <td>/api/patients</td>
        <td>GET</td>
        <td>Retrieves a list of all patients</td>
        <td>None</td>
        <td>JSON array of patient details</td>
    </tr>
    <tr>
        <td>/api/patients</td>
        <td>POST</td>
        <td>Creates a new patient</td>
        <td>JSON object with patient details (e.g., patient_id, patient_surname, etc.)</td>
        <td>Success message with created patient details</td>
    </tr>
    <tr>
        <td>/api/patients/&lt;id&gt;</td>
        <td>GET</td>
        <td>Retrieves details of a specific patient</td>
        <td>None</td>
        <td>JSON object with patient details</td>
    </tr>
    <!-- Assessment Endpoints -->
    <tr><td colspan="5"><b>Assessment Endpoints</b></td></tr>
    <tr>
        <td>/api/assessments</td>
        <td>GET</td>
        <td>Retrieves a list of all assessments</td>
        <td>None</td>
        <td>JSON array of assessment details</td>
    </tr>
    <tr>
        <td>/api/assessments</td>
        <td>POST</td>
        <td>Creates a new assessment</td>
        <td>JSON object with assessment details</td>
        <td>Success message with created assessment details</td>
    </tr>
    <tr>
        <td>/api/assessments/&lt;id&gt;</td>
        <td>GET</td>
        <td>Retrieves details of a specific assessment</td>
        <td>None</td>
        <td>JSON object with assessment details</td>
    </tr>
    <!-- Report Endpoints -->
    <tr><td colspan="5"><b>Report Endpoints</b></td></tr>
    <tr>
        <td>/api/sendreport</td>
        <td>POST</td>
        <td>Generates and sends a medical report</td>
        <td>JSON object with patient data</td>
        <td>Success message confirming report generation and sending</td>
    </tr>
    <!-- Latest Data Endpoint -->
    <tr><td colspan="5"><b>Latest Data Endpoint</b></td></tr>
    <tr>
        <td>/api/latest</td>
        <td>GET</td>
        <td>Retrieves the latest available data</td>
        <td>None</td>
        <td>JSON object with most recent data</td>
    </tr>
</table>






Link [deepnote.com](https://deepnote.com/workspace/Exercise-8e66c33b-eecd-42c8-bc44-7643f4fa0a86/project/TeamNexus-c9db920b-d439-4726-b52c-7a2b7d404be3/notebook/flask-app2-875a9f752d6743e3965809bb7b49cadb)



# External worker

# Benefits
1. Streamlined Workflow: A unified digital system eliminates inefficiencies and reduces manual workload.
2. Faster Discharge: Automation of document preparation ensures quicker discharge decisions.
3. Improved Accuracy: Standardized input forms and automated outputs minimize errors in documentation.
4. Enhanced Patient Autonomy: Self-scheduling follow-ups empower patients and reduce administrative burden.
5. Reduced Bottlenecks: Seamless communication between stakeholders avoids delays in the discharge process.
6. Time Savings: Automated workflows allow staff to focus on high-value patient care tasks

# Technologies
- Camunda
- Make
- Google Sheets
- Google Forms
- GMail
- Deepnote (for Python programming - Flask API/External worker/**LLM**)

# Conclusion
# Acknowledgments
# References
# Disclaimer
