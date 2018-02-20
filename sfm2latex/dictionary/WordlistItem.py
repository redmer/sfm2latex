from ..Latex import label, ref

LX_SEE_TEX_TEMPLATE = r'\hwsee{{{alternative}}}{{{headword}}}[{desc}]'


class WordlistItem(object):
    type = 'ht'

    def sk(self):
        return self._sk

    def __init__(self, sk='', ht_code='', desc='', instead_look_at=list()):
        super().__init__()
        self._sk = sk
        self.ht_code = ht_code
        self.desc = desc
        self.instead_look_at = instead_look_at

    def __repr__(self):
        return "{if_you_look_at} --> {instead_look_at}".format(
            if_you_look_at=self.ht_code,
            instead_look_at=', '.join(self.instead_look_at)
        )

    def render(self, settings={}):
        return LX_SEE_TEX_TEMPLATE.format(
            alternative=label(self.ht_code) + self.ht_code,
            headword=", ".join([ref(x) for x in self.instead_look_at]),
            desc=self.desc)
