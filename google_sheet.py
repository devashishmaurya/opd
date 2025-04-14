import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_google_sheet():
    # Define the scope of the application
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    
    # Use your credentials.json file to authenticate
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)

    # Open the Google Sheet using its unique key and return the first sheet
    sheet = client.open_by_key('1bFVKsoH9nlx_4rQDFwlsJXBAeQXDbVAvxa_a4FEEKLI').sheet1
    return sheet
