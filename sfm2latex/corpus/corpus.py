import os

from ..SFMFile import File
from ..utils import fix_orthography
from .Example import Example


def collect_examples(read_file):
    examples = list()
    current = None

    for mark, value in File(read_file):
        # Reference
        if 'ref' == mark:  # we have a new example
            if current is not None:
                examples.append(current)

            current = Example(value)

        # Morpheme boundaries (per word)
        elif 'mb' == mark:
            current.mb = value

        # Gloss English (per word)
        elif 'ge' == mark:
            current.ge = value

        # Free translation (English)
        elif 'ft' == mark:
            current.ft = value

        # Free comment
        elif 'cmt' == mark:
            current.cmt = value

    return examples


def render(index, settings={}):
    output = ''

    for item in index:
        output += item.render(settings) + '\n'

    return output


def build(input_filename, settings={}):
    # Get the lexemes from the SFM file
    examples = collect_examples(input_filename)

    # layout: {'aa' :  {001.tex, 002.tex, ...}, 'ab': {001.tex, 002.tex, ...}, ... }
    export = dict()

    for e in examples:
        if e.major() not in export:
            export[e.major()] = dict()

        export[e.major()][e.minor()] = e

    for major, maj_values in export.items():
        for minor, example in maj_values.items():
            target_file = 'output/{major}/{minor}.tex'.format(
                major=major,
                minor=minor
            )

            os.makedirs(os.path.dirname(target_file), exist_ok=True)
            out_file = open(target_file, 'w+')
            out_file.write(example.render(settings))
            out_file.close()
