import requests 

def send_report(report, target_url):
      headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(target_url, json=report, headers=headers)
        response.raise_for_status()  # Raise an error for bad HTTP responses
        return {"status": "success", "response": response.json()}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}