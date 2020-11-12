class Posting:
    def __init__(self, docID: int, url: str, freq: int):
        self.id = docID
        self.url = url
        self.freq = freq

    # Overriden __str__ to make it easier to debug when writing to file/console/etc
    # NOTICE: I do not print the url since it just clutters up the already massive index
    def __str__(self):
        return f'({self.id}, {self.freq})'