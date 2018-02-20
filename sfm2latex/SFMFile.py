from .utils import fix_orthography


UNKNOWN_TYPE = 'org.sil.toolbox.filetype.unknown'
DICTIONARY_TYPE = 'org.sil.toolbox.filetype.dictionary'
CORPUS_TYPE = 'org.sil.toolbox.filetype.corpus'


class SFMError(Exception):
    """Base class for Errors by SFM2Latex"""
    pass


class UnsupportedFileTypeError(SFMError):
    def __init__(self, path):
        super(UnsupportedFileTypeError, self).__init__()
        self.path = path


class File:
    """Detect the file type of the SFM file. 

    Currently supported types:
    - dictionary
    - text corpus
    """

    supported_manifests = [
        (DICTIONARY_TYPE, "\\_sh v3.0  804  MDF 4.0\n"),
        (CORPUS_TYPE, "\\_sh v3.0  804  Text\n"),
    ]

    def __init__(self, path):
        super().__init__()
        self.path = path
        self.type = UNKNOWN_TYPE

        with open(path) as file:
            self.firstline = file.readline()

        for identifier, manifest in self.supported_manifests:
            if self.firstline == manifest:
                self.type = identifier

    @classmethod
    def supported_types(cls):
        return [x[0] for x in cls.supported_manifests]

    def is_supported(self):
        return self.type != UNKNOWN_TYPE

    def is_dictionary(self):
        return self.type == DICTIONARY_TYPE

    def is_corpus(self):
        return self.type == CORPUS_TYPE

    def __iter__(self):
        """Iterator for the markers in the file.

        Values are filtered through a fix_orthography function. 
        Markers have the preceding slash removed.
        """
        with open(self.path, mode='r') as file:
            for line in file:
                if '\n' == line:
                    # empty lines can be safely skipped, as the algorithm does
                    # not rely on them
                    continue

                # remove the `\n` from the line
                line = line.strip()

                # split the value and the marker. According to SFM syntax, the
                # marker starts with backslash. The value starts with space. We
                # split on space and then remove the backslash.
                try:
                    mark, value = line.split(' ', 1)
                    mark = mark.lstrip('\\')

                except ValueError:
                    continue  # with the iteration

                # fix any orthographic problems
                value = fix_orthography(value)

                # yield to temporarily relinquish the point of execution
                yield (mark, value)
