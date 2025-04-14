import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Setup
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Try opening the sheet
sheet = client.open_by_key('1bFVKsoH9nlx_4rQDFwlsJXBAeQXDbVAvxa_a4FEEKLI').sheet1
print(sheet.get_all_records())
