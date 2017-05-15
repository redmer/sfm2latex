from .PartOfSpeech import PartOfSpeech
from .utils import sortkey, hyperref_to, capitalize_first, make_label


class Entry(object):
    LX_WORD_INHERITED_SYMBOL = ''
    LX_WORD_LOAN_SYMBOL = r'\textsuperscript{†}'

    type = 'entry'

    def __init__(self, hw):
        super().__init__()
        self.alts = list()
        self.parts_of_speech = [PartOfSpeech()]
        self.cfs = list()
        self.ec = ''
        self.es = list()
        self.hw = hw
        self.hm = ''
        self.inherited = 1
        self.mr = list()

    def __repr__(self):
        return "{hm}{headword}{alts}{u}\n{pos}\n{ety_sources}{ety_comment}{inherited}\n".format(
            hm=self.hm,
            headword=self.hw,
            alts=', '.join([''] + self.alts),
            u='\n\t(' + ' '.join([str(x) for x in self.mr]) + ')' if len(self.mr) else '',
            pos='\n'.join([str(x) for x in self.parts_of_speech]),
            ety_sources='\n'.join([str(x) for x in self.es]),
            ety_comment='\n\tEC\t' + self.ec if len(self.ec) else '',
            inherited='\n\tINH\t' + str(self.inherited),
        )

    def sk(self):
        return sortkey(self.hw + self.hm)

    def csv_render(self):
        return '"{hw}","{meaning}","{es}"'.format(
            hw=self.hw,
            meaning=self.parts_of_speech[0].senses[0].de[0],
            es=r', '.join([x.render() for x in self.es])
        )

    def render(self):
        def render_alts():
            return ', '.join(self.alts)

        def render_parts_of_speech():
            prefix = [] if len(self.parts_of_speech) > 1 else []
            return r'\\'.join(prefix + [x.render() for x in self.parts_of_speech])

        def render_cfs():
            return ', '.join([hyperref_to(x) for x in self.cfs])

        def render_hw():
            return self.hw

        def render_ec():
            if not len(self.ec):
                return ''
            if len(self.es):
                prefix = r'\ '
            else:
                prefix = ''
            # return prefix + r'$\diamondsuit$~' + self.ec
            return prefix + self.ec

        def render_es():
            if not len(self.es):
                return ''

            suffix = '' if self.es[-1].cert == 'dub' else '.'  # those need a '?'

            # return '\u27e6' + r', '.join([x.render() for x in self.es]) + '\u27e7'
            return capitalize_first(r', '.join([x.render() for x in self.es]) + suffix)

        def render_u():
            return ' '.join([hyperref_to(x) for x in self.mr]) if len(self.mr) else ''

        def render_etymology():
            # suffix = LX_WORD_INHERITED_SYMBOL if self.inherited > 0 else LX_WORD_LOAN_SYMBOL
            return render_es() + render_ec()# + suffix

        return r'\hwentry[{hm}]<{hw}{inh}>[{alts}]<{children}>[{cfs}][{ety}][{u}][{inhv}]'.format(
            hm=self.hm,
            inh=self.LX_WORD_INHERITED_SYMBOL if self.inherited > 0 else self.LX_WORD_LOAN_SYMBOL,
            hw=make_label(self.hw) + render_hw(),
            alts=render_alts(),
            cfs=render_cfs(),
            children=render_parts_of_speech(),
            ety=render_etymology(),
            u=render_u(),
            inhv=self.inherited
        ).replace('<', '{').replace('>', '}').replace('&lt;', '<').replace('&gt;', '>')
