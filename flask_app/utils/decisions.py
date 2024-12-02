def process_data(patient_data, inputs):

    # implement decision logic here
    decision = f"Processed data for {inputs["patient_id"]}"
    if patient["pain"] >= 7:
        return "register patient for rehab, prescribe painkillers"
    elif patient["pain"] >= 4:
        return "prescribe painkillers and physiotherapy"
    else:   
        return "physiotherapy only"