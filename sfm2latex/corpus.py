#!/usr/bin/python3

import os
from .Gloss import Gloss
from .utils import fix_orthography


def glosses_in_file(read_file):
    glosses = list()
    current_example = None

    for line in read_file.read().splitlines():
        if '' == line:  # skip empty lines
            continue

        try:
            marker, markervalue = line.split(' ', 1)
        except ValueError:
            continue  # with the iteration

        markervalue = fix_orthography(markervalue)

        if r'\ref' == marker:  # we have a new example
            if current_example is not None:
                glosses.append(current_example)

            current_example = Gloss(markervalue)

        if r'\tx' == marker:
            current_example.tx = markervalue

        elif r'\mb' == marker:
            current_example.mb = markervalue

        elif r'\ge' == marker:
            current_example.ge = markervalue

        elif r'\ps' == marker:
            current_example.ps = markervalue

        elif r'\ft' == marker:
            current_example.ft = markervalue

        elif r'\cmt' == marker:
            current_example.cmt = markervalue

        elif r'\ftn' == marker:
            current_example.ftn = markervalue

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
