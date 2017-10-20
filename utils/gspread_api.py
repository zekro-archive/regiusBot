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
        col2 = self.t.col_values(2)
        for i, k in enumerate(self.t.col_values(1)):
            if k != "":
                out[k] = col2[i]
        return out


    def set_dict(self, idict):
        """
        Sets the tables values from a given dictionary.
        """
        cellsA = self.t.range("A1:A" + str(len(idict.keys())))
        cellsB = self.t.range("B1:B" + str(len(idict.keys())))
        for i, c in enumerate(cellsA):
            c.value = list(idict.keys())[i]
        for i, c in enumerate(cellsB):
            c.value = list(idict.values())[i]
        cellsA.extend(cellsB)
        self.t.update_cells(cellsA)


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
    count = 1
    for t in table.col_values(1):
        if t != "":
            count += 1
        else:
            return count


def set_row_values(row, values, table):
    alph = "A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z".split(",")
    cells = table.range("A%d:%s%d" % (row, alph[len(values) - 1], row))
    print(len(cells))
    for i, c in enumerate(cells):
        c.value = values[i]
    table.update_cells(cells)


def append(values):
    gc = gspread.authorize(credentials)
    t = gc.open("dd_stats").sheet1
    set_row_values(get_next_row(t), values, t)


def test():
    append(["a", "b", "c", "d"])
    exit(0)
