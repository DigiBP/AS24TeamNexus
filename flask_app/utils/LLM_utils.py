from huggingface_hub import login
from transformers import pipeline

# Use your Hugging Face API key
api_key = "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"
login(api_key)

# Set the model you want to use
model_name = "HuggingFaceH4/zephyr-7b-beta"

# Initialize the pipeline with the model
generator = pipeline("text-generation", model=model_name, device=0)

def generate_report(patient_data):
    """
    Generates a report using Zephyr-7b-beta via the Hugging Face API
    based on the provided patient data.
    """
    prompt = f"""Generate a summary report of the medical conditions of a patient for post-surgery transfer to rehab:
    - Patient Name: {patient_data.get('name', 'N/A')}
    - Age: {patient_data.get('age', 'N/A')}
    - Surgery Date: {patient_data.get('surgery_date', 'N/A')}
    - Medication: {patient_data.get('medication', 'N/A')}
    - Recommendations: {patient_data.get('recommendations', 'N/A')}

    Report:"""

    # Use the model for generation
    result = generator(prompt, max_length=500, num_return_sequences=1, temperature=0.7)
    
    # Return the generated report (first sequence)
    return result[0]['generated_text']