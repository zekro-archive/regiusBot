import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('gsecrets.json', scope)


class Settings:
    def __init__(self, table, sheet):
        self.gc = gspread.authorize(credentials)
        self.t = self.gc.open(table).get_worksheet(sheet)

    def get_cval(self, x, y):
        """
        Get value of a cell by specified coordinates.
        """
        return self.t.cell(y, x).value

    def set_cval(self, x, y, val):
        """
        Set value of a cell by specified coordinates.
        """
        self.t.update_cell(y, x, val)

    def get_next_row(self):
        """
        Get the number of the next, empty row.
        """
        count = 1
        while len(self.t.row_values(count)[0]) > 0:
            count += 1
        return count

    def append(self, values):
        """
        Adds the values in the last, empty row. 
        """
        for i, v in enumerate(values):
            self.t.update_cell(self.get_next_row(), i + 1, v)

    def get_val(self, key):
        """
        Get the value and the row of the cell by key of a row.
        """
        count = 1
        while self.get_cval(1, count) != "":
            if self.get_cval(1, count) == key:
                return self.get_cval(2, count), count
            count += 1
        return None

    def get_key(self, val):
        """
        Get the key and the row of the cell by value of a row.
        """
        count = 1
        while self.get_cval(2, count) != "":
            if self.get_cval(2, count) == val:
                return self.get_cval(1, count), count
            count += 1
        return None

    def set_val(self, key, val):
        """
        Set the value by key.
        """
        self.set_cval(2, self.get_val(key)[1], val)

    def get_dict(self):
        """
        Returns the table as dictionary.
        """
        out = {}
        count = 1
        while self.get_cval(1, count) != "":
            out[self.get_cval(1, count)] = self.get_cval(2, count)
            count += 1
        return out

    def set_dict(self, idict):
        """
        Sets the tables values from a given dictionary.
        """
        count = 1
        for k, v in idict.items():
            self.set_cval(1, count, k)
            self.set_cval(2, count, v)
            count += 1



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
