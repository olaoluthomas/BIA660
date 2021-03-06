import csv

from collections import OrderedDict, Counter
from dateutil.parser import parse


class DataFrame(object):
    @classmethod
    def from_csv(cls, file_path, delimiting_character=',', quote_character='"'):
        with open(file_path, 'rU') as infile:
            reader = csv.reader(infile, delimiter=delimiting_character, quotechar=quote_character)
            data = []

            for row in reader:
                data.append(row)

            return cls(list_of_lists=data)

    def __init__(self, list_of_lists, header=True):
        # If headers already exist in the data, do this
        if header:
            self.header = list_of_lists[0]
            self.data = list_of_lists[1:]
            self.iterable = None
            self.row_of_rows = None

            # If any headers are duplicated, raise an exception
            if len(Counter(self.header).items()) < len(self.header):
                raise Exception('You have duplicate headers in your data')

        # If there are no headers in the data, create custom headers
        else:
            self.header = ['column' + str(index + 1) for index, column in enumerate(list_of_lists[0])]
            self.data = list_of_lists

        # Strip whitespace from all elements in all rows of the data
        for row in self.data:
            for key, value in enumerate(row):
                row[key] = value.strip()

        # Created an ordered dictionary from the data with headers as tags
        self.data = [OrderedDict(zip(self.header, row)) for row in self.data]

    def __getitem__(self, item):
        # this is for rows only
        if isinstance(item, (int, slice)):
            return self.data[item]

        # this is for columns only
        elif isinstance(item, (str, unicode)):
            return [row[item] for row in self.data]

        # this is for rows and columns
        elif isinstance(item, tuple):
            if isinstance(item[0], list) or isinstance(item[1], list):

                if isinstance(item[0], list):
                    rowz = [row for index, row in enumerate(self.data) if index in item[0]]
                else:
                    rowz = self.data[item[0]]

                if isinstance(item[1], list):
                    if all([isinstance(thing, int) for thing in item[1]]):
                        return [
                            [column_value for index, column_value in enumerate([value for value in row.itervalues()]) if
                             index in item[1]] for row in rowz]
                    elif all([isinstance(thing, (str, unicode)) for thing in item[1]]):
                        return [[row[column_name] for column_name in item[1]] for row in rowz]
                    else:
                        raise TypeError('What the hell is this?')

                else:
                    return [[value for value in row.itervalues()][item[1]] for row in rowz]
            else:
                if isinstance(item[1], (int, slice)):
                    return [[value for value in row.itervalues()][item[1]] for row in self.data[item[0]]]
                elif isinstance(item[1], (str, unicode)):
                    return [row[item[1]] for row in self.data[item[0]]]
                else:
                    raise TypeError('I don\'t know how to handle this...')

        # only for lists of column names
        elif isinstance(item, list):
            return [[row[column_name] for column_name in item] for row in self.data]

    def get_rows_where_column_has_value(self, column_name, value, index_only=False):
        if index_only:
            return [index for index, row_value in enumerate(self[column_name]) if row_value == value]
        else:
            return [row for row in self.data if row[column_name] == value]

    def get_column(self, column_name):
        if isinstance(column_name, str):
            return [row[column_name] for row in self.data]
        else:
            raise TypeError('You must pass a header of <type str> to retrieve data with column names')

    def min(self, column_name):
        self.iterable = [row[column_name].replace(',', '') for row in self.data]
        return min([float(string) if isfloat(string) else stringToDatetime(string) for string in self.iterable])

    def max(self, column_name):
        self.iterable = [row[column_name].replace(',', '') for row in self.data]
        return max([float(string) if isfloat(string) else stringToDatetime(string) for string in self.iterable])

    def sum(self, column_name):
        self.iterable = [row[column_name].replace(',', '') for row in self.data]
        return sum([float(string) if isfloat(string) else stringToDatetime(string) for string in self.iterable])

    def mean(self, column_name):
        return self.sum(column_name)/len(self[column_name])

    def median(self, column_name):
        self.iterable = sorted([row[column_name].replace(',', '') for row in self.data])
        self.iterable = [float(string) if isfloat(string) else stringToDatetime(string) for string in self.iterable]
        midd = len(self.iterable)/2
        if len(self.iterable) % 2 == 0:
            return (self.iterable[midd - 1] + self.iterable[midd]) / 2
        else:
            return self.iterable[midd]

    def std(self, column_name):
        mean = self.mean(column_name)
        return (sum([(convertDataType(item) - mean)**2 for item in self[column_name]])/len(self[column_name]))**0.5

    def add_rows(self, row_of_rows):
        if all([len(row) == len(self.header) for row in row_of_rows]):
            self.data.append([OrderedDict(zip(self.header, row)) for row in row_of_rows])
        else:
            raise Exception("Your data does not match the expected format")

    def add_column(self, new_col, column_name):
        if len(new_col) == len(self.data):
            self.header.append(column_name)
            for index, value in enumerate(new_col):
                self.data[index][column_name] = value
        else:
            raise Exception("Your data doesn't match!!!")

def convertDataType(string):
    string_no_comma = string.replace(',', '')
    if isfloat(string_no_comma):
        return float(string_no_comma)
    else:
        return stringToDatetime(string)

def isfloat(x):
    try:
        float(x)
        return True
    except:
        return False

def stringToDatetime(string):
    try:
        return parse(string)
    except:
        raise Exception('Invalid data type should be a float or timestamp string')

# sorted(test, key=lambda x: x[1], reverse=True)

df = DataFrame.from_csv('SalesJan2009.csv')
get_col = df.get_column('Payment_Type')
mns = df.min('Price')
mina = df.min('Transaction_date')
# minBad = df.min('Payment_Type')
mxs = df.max('Price')
sums = df.sum('Price')
means = df.mean('Price')
# medians = df.median('Payment_Type')
stddev = df.std('Price')

adding = df.add_rows([[value for value in df[1].itervalues()]])
# to test get_col
# get_col2 = df.get_column(2)

# to test that only successfully converted floats will be passed
# mina = df.min('Payment_Type')

# testing std instance method
# stddev_2 = df.std('Payment_Type')

# two plus two
2 + 2