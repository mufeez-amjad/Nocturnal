import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('Nocturnal-7d790916f958.json', scope)

gc = gspread.authorize(credentials)

wks = gc.open('Nocturnal').sheet1

# wks.delete_row(2)

# print(wks.get_all_records())

#dictionary with rows
# wks.append_row(['this goes into first column', 'this goes into second column'])

# print(wks.acell('A2'))
# print(wks.cell(2,1).value) #row 2 column 1 .col return column, .row returns row .value returns value at cell

# wks.update_acell('B2', "This is B2")
# wks.update_cell(3,2, "This is B3")

# print(wks.find('Test')) #findall if theres duplicates

list_of_cells = wks.findall('Test')

for cell in list_of_cells:
  cell.value = 'Looped value'
# list_of_cells[2].value = 'New value'

wks.update_cells(list_of_cells)