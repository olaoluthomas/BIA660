from collections import OrderedDict

class DataFrame(object):
    def __init__(self, list_of_lists, header=True):
        if header:
            self.header = list_of_lists[0]
            self.data = list_of_lists[1:]
        else:
            self.header = ['column' + str(index + 1) for index, column in enumerate(self.data[0])]
            self.data = list_of_lists

        self.data = [OrderedDict(zip(self.header, row)) for row in self.data]

    def __getitem__(self, item):
        # this is for rows only
        if isinstance(item, (int, slice)):
            return self.data[item]

        # this is for columns only
        elif isinstance(item, (str, unicode)):
            return [row[item] for row in self.data]

        # this is for rows and columns
        else:
            if isinstance(item[0], list) or isinstance(item[1], list):

                if isinstance(item[0], list):
                    rowz = [row for index, row in enumerate(self.data) if index in item[0]]
                else:
                    rowz = self.data[item[0]]

                if isinstance(item[1], list):
                    return [[column_value for index, column_value in enumerate([value for value in row.itervalues()]) if index in item[1]] for row in rowz]
                else:
                    return [value for value in row.itervalues()[item[1]] for row in rowz]
            else:
                return [row[item[1]]for row in self.data[item[0]]]

infile = open('SalesJan2009.csv')
lines = infile.readlines()
lines = lines[0].split('\r')
data = [l.split(',') for l in lines]
things = lines[559].split('"')
data[559] = things[0].split(',')[:-1] + [things[1]] + things[2].split(',')[1:]


df = DataFrame(list_of_lists=data)
# get the 5th row
fifth = df[4]

# get the 5th to 10th row
sliced = df[4:10]

# get item definition for df [row, column]

# get the third column of all rows
tupled = df[:, 2]

# get the 2nd column of the 1st 5 rows
tupled_slices = df[0:5, :3]

# get the 2nd and 5th column of the 2nd and 5th rows
tupled_bits = df[[1, 4], [1, 4]]

# adding header for data with no header
df = DataFrame(list_of_lists=data[1:], header=False)

# fetch columns by name
named = df['column1']

2+2