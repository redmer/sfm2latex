"""Utilities for LaTeX output"""

from .utils import sortkey

TEX_LABEL_TEMPLATE = r'zz-LABEL'
TEX_LABEL_COMMAND = r'\label{REF_TARGET}'
TEX_REF_COMMAND = r'\hyperref[REF_TARGET]{REF_FROM}'


def label(word):
    """Generates a label for a word (item)."""
    return f"\\label{{zz-{sortkey(word)}}}"


def ref(word, label=None):
    """A LaTeX hyperref reference to a word."""
    if label is None:
        label = sortkey(word)
    return f'\\hyperref[zz-{label}]{{{word}}}'
