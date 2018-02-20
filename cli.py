import json
import sys

import click

from sfm2latex import corpus, dictionary
from sfm2latex.SFMFile import File, UnsupportedFileTypeError


@click.command()
@click.argument('input_paths', nargs=-1, type=click.Path(exists=True))
@click.option('--output', type=click.Path(), required=True)
@click.option('--config', type=click.Path(exists=True), help="a configuration file.")
def main(input_paths, output, config):
    """Convert SIL’s Toolbox SFM files into LaTeX files.

    See <https://github/redmer/sfm2latex> for a specification of all required
    files."""

    # Collect all input_file arguments per supported type
    dictionary_files = list()
    corpus_files = list()

    for path in input_paths:
        file = File(path)

        if file.is_dictionary():
            dictionary_files.append(file)

        elif file.is_corpus():
            corpus_files.append(file)

        else:
            # do not silently ignore unsupported files.
            raise UnsupportedFileTypeError(path)

    # Load options
    with open(config) as configuration_path:
        settings = json.load(configuration_path)

    for file in dictionary_files:
        dictionary.build(file.path, settings=settings)

    for file in corpus_files:
        corpus.build(file.path, settings=settings)
