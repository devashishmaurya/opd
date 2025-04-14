import gspread
from oauth2client.service_account import ServiceAccountCredentials

def append_to_google_sheet(data):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key('1bFVKsoH9nlx_4rQDFwlsJXBAeQXDbVAvxa_a4FEEKLI').sheet1

    row = [
        data['patient_name'],
        data['age'],
        data['gender'],
        data['slip_note_time'],
        data['doctor_name'],
        data['created_by']
    ]

    # Append the row and return the token number (row number)
    row_number = len(sheet.get_all_values()) + 1  # Get the new row number
    sheet.append_row(row)
    
    return row_number  # Return the token number (row number)
