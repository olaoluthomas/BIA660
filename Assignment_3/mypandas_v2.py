import csv

from collections import OrderedDict, Counter, defaultdict
from dateutil.parser import parse


# from operator import itemgetter


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
            self.sorted_data = None

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
            return Series([tryConvertDataType(row[item]) for row in self.data])

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
            if all(isinstance(thing, bool) for thing in item):
                comp_list = []
                for index, row in enumerate(self.data):
                    if item[index]:
                        comp_list.append(row)
                return comp_list
            else:
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
        return min([convertDataType(string) for string in self.iterable])

    def max(self, column_name):
        self.iterable = [row[column_name].replace(',', '') for row in self.data]
        return max([convertDataType(string) for string in self.iterable])

    def sum(self, column_name):
        self.iterable = [row[column_name].replace(',', '') for row in self.data]
        return sum([convertDataType(string) for string in self.iterable])

    def mean(self, column_name):
        return self.sum(column_name) / len(self[column_name])

    def median(self, column_name):
        self.iterable = sorted([row[column_name].replace(',', '') for row in self.data])
        self.iterable = [convertDataType(string) for string in self.iterable]
        midd = len(self.iterable) / 2
        if len(self.iterable) % 2 == 0:
            return (self.iterable[midd - 1] + self.iterable[midd]) / 2
        else:
            return self.iterable[midd]

    def std(self, column_name):
        mean = self.mean(column_name)
        return (
               sum([(convertDataType(item) - mean) ** 2 for item in self[column_name]]) / len(self[column_name])) ** 0.5

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

    # the syntax is sorted(test, key=lambda x: x[1], reverse=True)
    # sorts the entire dataframe by the column name passed either in ascending or descending order
    def sort_by(self, column_name, desc=False):
        if isinstance(column_name, str):
            self.sorted_data = sorted(self.data, key=lambda row: row[column_name], reverse=desc)
            return self.sorted_data
        elif isinstance(column_name, list) & isinstance(desc, list):
            for index, value in enumerate(column_name):
                self.sorted_data = sorted(self.data, key=lambda row: row[value], reverse=desc[index])
                return self.sorted_data
        else:
            raise Exception("You've got your syntax all wrong!")

    # for
    def group_by(self, column_name, agg_column):
        if isinstance(column_name, str) & isinstance(agg_column, str):
            dd = defaultdict(list)
            for index, value in enumerate(self[column_name]):
                dd[value].append(self[agg_column][index])
            return dd
        else:
            raise Exception('Something\'s missing...')

def avg(list):
    return sum(list)/len(list)

def max(x):
    return max(list)

def min(x):
    return min(list)

class Series(list):
    def __eq__(self, other):
        ret_list = []

        for item in self:
            ret_list.append(item == other)

        return ret_list

    def __ne__(self, other):
        ret_list = []

        for item in self:
            ret_list.append(item != other)

        return ret_list

    def __gt__(self, other):
        ret_list = []

        for item in self:
            ret_list.append(item > other)

        return ret_list

    def __lt__(self, other):
        ret_list = []

        for item in self:
            ret_list.append(item < other)

        return ret_list

    def __ge__(self, other):
        ret_list = []

        for item in self:
            ret_list.append(item >= other)

        return ret_list

    def __le__(self, other):
        ret_list = []

        for item in self:
            ret_list.append(item <= other)

        return ret_list


def convertDataType(string):
    string_no_comma = string.replace(',', '')
    if isfloat(string_no_comma):
        return float(string_no_comma)
    else:
        try:
            return parse(string_no_comma)
        except:
            raise Exception('Invalid data type. Must be a float or timestamp string')


def tryConvertDataType(string):
    if isfloat(string):
        return float(string)
    else:
        try:
            return parse(string)
        except:
            return string


def isfloat(x):
    try:
        float(x)
        return True
    except:
        return False


df = DataFrame.from_csv('SalesJan2009.csv')
# get_col = df.get_column('Payment_Type')
# mns = df.min('Price')
# mina = df.min('Transaction_date')
# minBad = df.min('Payment_Type')
# mxs = df.max('Price')
# sums = df.sum('Price')
# means = df.mean('Price')
# medians = df.median('Payment_Type')
# stddev = df.std('Price')
# adding = df.add_rows([[value for value in df[1].itervalues()]])

# sort = df.sort_by('Transaction_date')
# sorts = df.sort_by(['City', 'Transaction_date'], [False, True])
# comp = df[df['Payment_Type'] == 'Mastercard']
grp = df.group_by('Payment_Type', 'Price')
# to test get_col
# get_col2 = df.get_column(2)
# to test that only successfully converted floats will be passed
# mina = df.min('Payment_Type')

# testing std instance method
# stddev_2 = df.std('Payment_Type')

# two plus two
2 + 2
