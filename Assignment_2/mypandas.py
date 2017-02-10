import csv

from collections import OrderedDict, Counter

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

            # If any headers are duplicated, raise TypeError
            if len(Counter(self.header).items()) < len(self.header):
                raise TypeError('You have duplicate headers in your data')

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
                        return [[column_value for index, column_value in enumerate([value for value in row.itervalues()]) if index in item[1]] for row in rowz]
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
            raise KeyError('You must pass a header of <type str> to retrieve data in columns')


    def min(self, column_name):
        if isinstance(column_name, str):
            self.iterable = [float(row[column_name].replace(',','')) for row in self.data]
            return min(self.iterable)
        else:
            return KeyError('Invalid data type...')

    def max(self, column_name):
        if isinstance(column_name, str):
            self.iterable = [float(row[column_name].replace(',','')) for row in self.data]
            return max(self.iterable)
        else:
            return KeyError('Invalid data type...')

    def sum(self, column_name):
        if isinstance(column_name, str):
            self.iterable = [float(row[column_name].replace(',','')) for row in self.data]
            return sum(self.iterable)
        else:
            return KeyError('Invalid data type...')

    def median(self, column_name):
        self.iterable = None
        if isinstance(column_name, str):
            self.iterable = [float(row[column_name].replace(',','')) for row in self.data]
            self.iterable.sort()
            if len(self.iterable) % 2:
                return (self.iterable[len(self.iterable)/2 - 1] + self.iterable[len(self.iterable)/2])/2
            else:
                return self.iterable[len(self.iterable)/2]



df = DataFrame.from_csv('SalesJan2009.csv')
get_col = df.get_column('Price')
mins = df.min('Price')
maxs = df.max('Price')
sums = df.sum('Price')
medians = df.median('Price')

# mina = df.min['Payment_Type'] to test that only successfully converted floats will be passed
# two plus two
2+2
