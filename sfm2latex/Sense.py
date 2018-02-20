from .utils import capitalize_first
from .Latex import ref


class Sense(object):
    type = 'sense'

    def __init__(self):
        super().__init__()
        self.ge = ''  # gloss (prelim. implementation)
        self.dn = list()  # national definition
        self.de = list()  # english definition
        self.re = list()  # index english
        self.rn = list()  # index national
        self.sc = ''  # scientific name
        self.ht = list()  # haspelmath & tadmor 1460 number
        self.nt = ''  # note
        self.img_src = ''  # pc : image src
        self.img_attrib = ''  # pc : image attrib

    def __repr__(self):
        return "\n\t\t- {english}{sc}{note}".format(
            english='\n\t\t- '.join(self.de),
            sc='\n\tSC\t' + self.sc if len(self.sc) else '',
            note=('\n\tNT\t' + self.nt.strip()) if len(self.nt) else ''
        )

    # Rendering is dependent on what elements are filled in
    def render(self):
        def render_english():
            try:
                if ',' in self.de[0]:
                    first_part, second_part = self.de[0].split(',', 1)
                    self.de[0] = r'\textbf<' + \
                        capitalize_first(first_part.strip()) + \
                        r'>, ' + second_part.strip()
                elif self.de[0][0:2] == ' \\':
                    self.de += [self.de.pop(0).strip()]
                else:
                    self.de[0] = r'\textbf<' + \
                        capitalize_first(self.de[0].strip()) + r'>'

                return ', '.join(self.de)
            except IndexError as e:
                print(e)

        def render_national():
            if len(self.dn):
                self.dn[0] = capitalize_first(self.dn[0])
                return '(' + ', '.join(self.dn) + ').'
            raise ValueError('A meaning is missing in', self.de)
            # return ''

        def render_note():
            return self.nt.strip()  # (self.nt + ' ') if len(self.nt) else ''

        def render_ht():
            return ', '.join([ref(x) for x in self.ht]) if len(self.ht) else ''

        return r'\hwsense<{english}. {national}>[{linnaeus}][{nt}][{ht}]'.format(
            english=capitalize_first(render_english()),
            national=capitalize_first(render_national()),
            linnaeus=self.sc,
            nt=render_note(),
            ht=render_ht(),
        )
