#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
from sfm2latex import corpus, dictionary

import argparse


def main(argv):
    parser = argparse.ArgumentParser(description='Convert SIL’s Toolbox SFM files to LaTeX files.')
    parser.add_argument(
        '--dictionary',
        nargs=1,
        # type=argparse.FileType('r', 'encoding=UTF-8'),
        help='Provide a dictionary file. See <https://github/redmer/sfm2latex> for a spec.',
        metavar='DICTIONARY.txt',
        dest='dictionary'
    )
    parser.add_argument(
        '--corpus',
        nargs=1,
        # type=argparse.FileType('r', 'encoding=UTF-8'),
        help='Provide a corpus file. See <https://github/redmer/sfm2latex> for a spec.',
        metavar='CORPUS.txt',
        dest='corpus'
    )
    args = parser.parse_args()

    dictionary_filename = vars(args)['dictionary'][0]
    corpus_filename = vars(args)['corpus'][0]
    if dictionary_filename is None and corpus_filename is None:
        # Two empty arguments
        parser.error('Please supply a dictionary and/or a corpus file.')

    # Load options
    settings_file = open('build-settings.json')
    settings = json.load(settings_file)
    settings_file.close()

    corpus.build(corpus_filename, settings=settings)
    dictionary.build(dictionary_filename, settings=settings)

    sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
