import tile


class Map:
    def __init__(self):
        self.map:list[list[int]]

    def load(mapname):
        with open(mapname) as file:
            for line in file.readlines():
                idstr = line.split(',')
                for i in idstr:
                    id = int(i)

    