import re

from ..utils import capitalize_first, escape_for_latex


TEX_GLOSS_ENVIRONMENT = r'''\ex~\begingl
\gla {mb}//
\glb {ge}//
\glft `{ft}'{cmt}\label{{{label}}}\trailingcitation{{[{cit}]}}//
\endgl\xe'''


class Example(object):
    """Represent a single example sentence from a Texts.txt file."""
    type = 'example'

    def __init__(self, reference_key):
        super().__init__()
        self.ref = reference_key
        self.mb = ''
        self.ge = ''
        self.ft = ''
        self.cmt = ''

        # We need to strip off whitespace *before* bound morphemes
        self.whitespace_stripper = re.compile(r'(\s+)-')

    def major(self):
        """The part before the last period in ref, without periods."""
        return self.ref.rsplit('.', 1)[0].replace('.', '')

    def minor(self):
        """The part after the last period in ref, without periods."""
        return self.ref.rsplit('.', 1)[1].replace('.', '')

    def render(self, settings={}):
        def render_label():
            return self.ref.replace('.', '')

        def render_mb():
            return self.whitespace_stripper.sub('-', self.mb)

        def render_ge():
            return self.whitespace_stripper.sub('-', self.ge)

        def render_ft():
            return capitalize_first(self.ft.strip())

        def render_cmt():
            return '' if len(self.cmt) < 1 else r'\\(' + capitalize_first(self.cmt.strip()) + ')'

        return settings['render']['Example'].format(
            mb=render_mb(),
            ge=escape_for_latex(render_ge()),
            label=render_label(),
            ft=render_ft(),
            cit=self.ref,
            cmt=render_cmt(),
        )
