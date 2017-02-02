class DataFrame(object):
    def __init__(self, list_of_lists, header=True):
        if header:
            self.data = list_of_lists
            self.header = list_of_lists[0]
        else:
            self.data = list_of_lists

    def __getitem__(self, item):
        self.data[item]

infile = open('SalesJan2009.csv')
lines = infile.readlines()
lines = lines[0].split('\r')
data = [l.split(',') for l in lines]
things = lines[559].split('"')

df = DataFrame(data)
# get the 4th row
df[4]