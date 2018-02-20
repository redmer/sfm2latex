HEADING_TEX_TEMPLATE = r'\lettergroup{{{title}}}'
REVERSE_HEADING_TEX_TEMPLATE = r'\wordlistsection*{{{title}}}'
HT_HEADING_TEX_TEMPLATE = r'\wordlistsection*{{{title}}}'


class WordlistHeader(object):
    type = 'header'

    def sk(self):
        return self._sk

    def __init__(self, sk='', desc='', level='vernacular'):
        super().__init__()
        self._sk = sk if len(sk) else desc
        self.desc = desc
        self.level = level

    def __repr__(self):
        return self.desc

    def render(self, settings={}):
        if self.level == 'vernacular':
            return HEADING_TEX_TEMPLATE.format(title=self.desc)
        elif self.level == 'ht':
            return HT_HEADING_TEX_TEMPLATE.format(title=self.desc)
        elif self.level == 'reverse':
            return REVERSE_HEADING_TEX_TEMPLATE.format(title=self.desc)
