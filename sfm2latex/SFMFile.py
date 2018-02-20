
class UnsupportedFileTypeError(Exception):
    pass


DICTIONARY_TYPE = 'dictionary'
UNKNOWN_TYPE = 'unknown'
CORPUS_TYPE = 'corpus'


class File:
    """Detect the file type of the SFM file. 

    Currently supported types:
    - dictionary
    - text corpus
    """

    type_ids = [
        (DICTIONARY_TYPE, "\\_sh v3.0  804  MDF 4.0\n"),
        (CORPUS_TYPE, "\\_sh v3.0  804  Text\n"),
    ]

    def __init__(self, path):
        super().__init__()
        self.path = path
        self.type = UNKNOWN_TYPE

        with open(path) as file:
            self.firstline = file.readlines()[0]

        for identifier, version_string in self.type_ids:
            if self.firstline == version_string:
                self.type = identifier

    @classmethod
    def supported_types(cls):
        return [x[0] for x in cls.type_ids]

    def is_supported(self):
        return self.type != UNKNOWN_TYPE

    def is_dictionary(self):
        return self.firstline == DICTIONARY_TYPE

    def is_corpus(self):
        return self.firstline == CORPUS_TYPE
