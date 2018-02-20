#!/usr/bin/python3

import os

from ..SFMFile import File
from ..utils import fix_orthography
from .Gloss import Gloss


def glosses_in_file(read_file):
    glosses = list()
    current_example = None

    for mark, value in File(read_file):
        if 'ref' == mark:  # we have a new example
            if current_example is not None:
                glosses.append(current_example)

            current_example = Gloss(value)

        if 'tx' == mark:
            current_example.tx = value

        elif 'mb' == mark:
            current_example.mb = value

        elif 'ge' == mark:
            current_example.ge = value

        elif 'ps' == mark:
            current_example.ps = value

        elif 'ft' == mark:
            current_example.ft = value

        elif 'cmt' == mark:
            current_example.cmt = value

        elif 'ftn' == mark:
            current_example.ftn = value

    return glosses


def render(index):
    output = ''

    for item in index:
        output += item.render() + '\n'

    return output


def build(input_filename, settings={}):
    in_file = open(input_filename)

    # Get the lexemes from the SFM file
    examples = glosses_in_file(in_file)

    # layout: {'aa' :  {001, 002, ...}, 'ab': {001, 002, ...}, ... }
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
            out_file.write(example.render())
            out_file.close()
