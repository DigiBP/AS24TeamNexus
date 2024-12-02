# this is just a test script to see if it works!

from utils.google_sheets import get_patient_data

def test_google_sheet():
    sheet_name = "patient_data" 
    data = get_patient_data(sheet_name)
    if data:
        print("Data retrieved successfully:")
        for row in data:
            print(row)
    else:
        print("No data found or an error occurred.")

if __name__ == "__main__":
    test_google_sheet()

# Run the test script:

test_google_sheet()