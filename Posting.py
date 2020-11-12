class Posting:
    def __init__(self, docID: int, freq: int):
        self.id = docID
        # self.url = url
        self.freq = freq

    # Overriden __str__ and __repr__ to make it easier to debug when writing to file/console/etc
    def __str__(self):
        return f'({self.id}, {self.freq})'

    def __repr__(self):
        return f'Posting({self.id}, {self.freq})'