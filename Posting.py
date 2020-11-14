class Posting:
    def __init__(self, docID: int, tf_idf: int):
        self.id = docID
        # self.url = url
        self.tf_idf = tf_idf

    # Overriden __str__ and __repr__ to make it easier to debug when writing to file/console/etc
    def __str__(self):
        return f'({self.id}, {self.tf_idf})'

    def __repr__(self):
        return f'Posting({self.id}, {self.tf_idf})'