# Team Nexus 
### Patient Discharge Process after Total-Hip-Replacement Surgery

# Team members
Elisa Hemmig,
Justin Jouwena,
Dominique Jud,
Ramon Winkler,

# Coaches
Andreas Martin
Devid Montecchiari
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
# Flask API
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
