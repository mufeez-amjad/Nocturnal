from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

# The ID and range of a sample spreadsheet.
spreadsheet_id = '1RJhe1jhH83FbOgCX6tFce6c6rfCSPM-iPrq2uelVhXQ'
range_name = 'Sheet1!A:A'
value_input_option = 'RAW'

def main():
    #gets auth for sheet id
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    sheet = service.spreadsheets()

    values = [
        [
            "Hello", "World"
        ],
        # Additional rows ...
    ]
    body = {
        'values': values
    }
    result = sheet.values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption=value_input_option, body=body).execute()

    print('{0} cells updated.'.format(result.get('updatedCells')))

    # result = sheet.values().get(spreadsheetId=spreadsheet_id,
    #                             range=range_name).execute()
    # values = result.get('values', [])

    # if not values:
    #     print('No data found.')
    # else:
    #     for row in values:
    #         print('%s' % (row[0]))

if __name__ == '__main__':
    main()