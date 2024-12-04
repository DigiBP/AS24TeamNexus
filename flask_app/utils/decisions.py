def process_data(patient_data, inputs):

    # implement decision logic here
    decision = f"Processed data for {inputs["patient_id"]}"
    if patient["pain"] >= 7:
        return "register patient for rehab, prescribe painkillers"
    elif patient["pain"] >= 4:
        return "prescribe painkillers and physiotherapy"
    else:   
        return "physiotherapy only"


if  age > 65:
    return "reha and painkillers"
elif age > 40:
    return "physio and painkillers"
else:
    return "pain killers only"

if pain > 7:
    return "high pain"