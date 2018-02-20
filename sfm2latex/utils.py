import sys


def sortkey(foreign_word):
    """
    Generates a predictable sortkey to sort Quechua words on. Also used
    for `hyperref` references in the document. 
    """
    foreign_word = foreign_word \
        .lower() \
        .replace(r'\textsuperscript{†}', '') \
        .replace('!', '') \
        .replace('¡', '') \
        .replace('(', '') \
        .replace(')', '') \
        .replace('=', '') \
        .replace('-', '') \
        .replace('ch', 'cπ')

    foreign_word = foreign_word \
        .replace("ph", "pπ") \
        .replace("th", "tπ") \
        .replace("cπh", "cππ") \
        .replace("kh", "kπ") \
        .replace("qh", "qπ")

    foreign_word = foreign_word \
        .replace("'", "ππ")

    foreign_word = foreign_word \
        .replace("\uA741", "k") \
        .replace("\uA757", "q")  # sort k-with-stroke and q-with-stroke as -without-stroke

    foreign_word = foreign_word \
        .replace("ll", "lπ") \
        .replace("ñ", "nπ") \
        .replace(" ", "-")

    return foreign_word.lower()


def capitalize_first(x):
    """
    This function upper-cases only the first letter, unlike
    .capitalize() that leaves the other letters uppercase. It 
    leaves other letters as they were.
    """
    return x[0].capitalize() + x[1:] if len(x) > 0 else x


TEX_GLOSS_REPL = list()


def fix_orthography(input):
    return input.replace('ꝗ', r'q̄') \
                .replace('ꝁ', r'ḵ')


def escape_for_latex(string):
    string = string.replace('\\', r'\textbackslash{}')

    if len(TEX_GLOSS_REPL) < 1:
        glosses_file = open('data/glossing-abbreviations.csv')
        for line in glosses_file.read().splitlines():
            try:
                abbr, leipzig = line.split(',', 1)
                TEX_GLOSS_REPL.append((abbr, leipzig))
            except ValueError:
                print('There was an error parsing "' + str(line) + '" in the custom glosses file.\n'
                      'A comma needs to separate two values. No more, no less.\n'
                      'Please correct this error and try again.', file=sys.stderr)
                sys.exit(2)
        glosses_file.close()
        TEX_GLOSS_REPL.sort(key=lambda x: len(x[0]), reverse=True)

    for search, repl in TEX_GLOSS_REPL:
        string = string.replace(search, repl)

    return string
