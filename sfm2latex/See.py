from .utils import sortkey
from .Latex import ref

LX_SEE_TEX_TEMPLATE = r'\hwsee{{{alternative}}}{{{headword}}}[{desc}]'
LX_SEE_SUBORDINATE_TEX_TEMPLATE = r'\hwseesubord{{{alternative}}}{{{headword}}}[{desc}]'


class See(object):
    type = 'see'

    def sk(self):
        suffix = 'π' if self.is_subordinate else ''
        if self.sort_as_vernacular:
            return sortkey(self.if_you_look_at) + suffix

        return self.if_you_look_at + suffix

    def __repr__(self):
        return "{if_you_look_at} --> {instead_look_at}".format(
            if_you_look_at=self.if_you_look_at,
            instead_look_at=', '.join(self.instead_look_at)
        )

    def __init__(self, instead_look_at=None, if_you_look_at='', sort_as_vernacular=True, is_subordinate=False):
        super().__init__()
        if instead_look_at is None:
            instead_look_at = []

        self.instead_look_at = instead_look_at
        self.if_you_look_at = if_you_look_at
        self.sort_as_vernacular = sort_as_vernacular
        self.is_subordinate = is_subordinate

    def render(self):
        template = LX_SEE_SUBORDINATE_TEX_TEMPLATE if self.is_subordinate else LX_SEE_TEX_TEMPLATE

        def render_alternative():
            return self.if_you_look_at.split(', ', 1)[-1] if self.is_subordinate else self.if_you_look_at

        return template.format(
            alternative=render_alternative(),
            headword=', '.join([ref(x) for x in self.instead_look_at]),
            desc='').replace('&lt;', '<').replace('&gt;', '>')
