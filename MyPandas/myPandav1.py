class DataFrame(object):
    def __init__(self, list_of_lists, header=True):
        if header:
            self.header = list_of_lists[0]
            self.data = list_of_lists[1:]
        else:
            self.data = list_of_lists

    def __getitem__(self, item):
        # this is for rows only
        if isinstance(item, (int, slice)):
            return self.data[item]
        else:
            if isinstance(item[0], list) or isinstance(item[1], list):
                rowz = None
                if isinstance(item[0], list):
                    rowz = [row for index, row in enumerate(self.data) if index in item[0]]
                else:
                    rowz = self.data(item[0])

                if isinstance(item[1], list):
                    return [[column for index, column in enumerate(row) if index in item[1]] for row in rowz]
                else:
                    return [row[item[1]] for row in rowz]
            else:
                return [row[item[1]] for row in self.data[item[0]]]

infile = open('SalesJan2009.csv')
lines = infile.readlines()
lines = lines[0].split('\r')
data = [l.split(',') for l in lines]
things = lines[559].split('"')
data[559] = things[0].split(',')[:-1] + [things[1]] + things[2].split(',')[1:]


df = DataFrame(list_of_lists=data)
# get the 5th row
fifth = df[4]
sliced = df[4:10]

# get item definition for df [row, column]

# get the third colum
tupled = df[:, 2]
tupled_slices = df[0:5, :3]
tupled_bits = df[[1, 4], [1, 4]]

2+2