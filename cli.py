import json
import sys
from pathlib import Path

import click

from sfm2latex import corpus
from sfm2latex.SFMFile import File, UnsupportedFileTypeError


@click.command()
@click.argument('input_paths', nargs=-1, type=click.Path(exists=True))
@click.option('--output', type=click.Path(), required=True)
@click.option('--verbose', is_flag=True)
@click.option('--config', type=click.Path(exists=True), help="a configuration file.")
def main(input_paths, output, config, verbose=False):
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
            # raise UnsupportedFileTypeError(path)
            click.echo(
                f"File '{path}' not supported. "
                f"Supported file types: {File.supported_types()}.")
            click.echo('Conversion stopped.')
            sys.exit(500)

    if verbose:
        click.echo(f'Dictionary files: {len(dictionary_files)}')
        click.echo(f'Corpus files:     {len(corpus_files)}')

    # Load options from JSON file
    if config:
        with open(config) as settings:
            settings = json.load(settings)
    else:
        # Load default configuration
        p = Path(__file__).resolve()
        config_path = p.parent / 'build-settings.json'
        with open(config_path) as settings:
            settings = json.load(settings)

    for file in dictionary_files:
        pass
        # dictionary.build(file.path, settings=settings)

    for file in corpus_files:
        corpus.build(file.path, settings=settings)
