import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('gsecrets.json', scope)


def get_next_row(table):
    count = 1
    while len(table.row_values(count)[0]) > 0:
        count += 1
    return count


def set_row_values(row, values, table):
    for i, v in enumerate(values):
        table.update_cell(row, i + 1, v)


def append(values):
    gc = gspread.authorize(credentials)
    t = gc.open("dd_stats").sheet1
    set_row_values(get_next_row(t), values, t)
