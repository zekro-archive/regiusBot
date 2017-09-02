import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('gsecrets.json', scope)


class Settings:
    def __init__(self, table, sheet):
        self.gc = gspread.authorize(credentials)
        self.t = self.gc.open(table).get_worksheet(sheet)

    def get_cval(self, x, y):
        return self.t.cell(y, x).value

    def set_cval(self, x, y, val):
        self.t.update_cell(y, x, val)

    def get_next_row(self):
        count = 1
        while len(self.t.row_values(count)[0]) > 0:
            count += 1
        return count

    def append(self, values):
        for i, v in enumerate(values):
            self.t.update_cell(self.get_next_row(), i + 1, v)

    def get_val()


def get_stats():
    gc = gspread.authorize(credentials)
    t = gc.open("dd_stats").sheet1

    def _g(x, y):
        return t.cell(y, x).value
    out = []
    for i in range(2, 11):
        out.append(_g(8, i))
    return out


def get_next_row(table):
    count = 1560
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
