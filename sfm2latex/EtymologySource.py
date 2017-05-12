class EtymologySource(object):
    type = 'etymology_lang'

    langdict = {
        'Aym': 'Aymara!in lexicon',
        'PAym': 'Proto-Aymara!in lexicon',
        'PQue': 'Proto-Quechua!in lexicon',
        'Que': 'Quechua!in lexicon',
        'PQueAym': 'Proto-Quechumaran!in lexicon',
        'Kall': 'Kallawaya!in lexicon',
        'Uch': 'Uchumataqu!in lexicon',
        'U-Ch': 'Uru-Chipaya!in lexicon',
        'Sp': 'Spanish!in lexicon',
    }

    sourcedict = {
        'CENAQ': '\CENAQ'
    }

    def __init__(self, lang, cert, value):
        super().__init__()
        if lang in self.langdict:
            self.lang = lang + r'\il{' + self.langdict[lang] + r'}'
        elif lang in self.sourcedict:
            self.lang = self.sourcedict[lang]
        else:
            self.lang = lang
        self.cert = cert
        self.value = value if len(value) else ''

    def __repr__(self):
        return "\tES\t{lang} {value}".format(
            cert=self.cert,
            lang=self.lang,
            value=self.value
        )

    def render(self):
        def render_lang():
            return self.lang.strip() + ' ' if len(self.value.strip()) else self.lang.strip()

        def render_value():
            return self.value.replace(r' \emlen', r'\emlen').strip()

        def render_lang_value():
            return r'{lang}{value}'.format(
                lang=render_lang(),
                value=render_value(),
            )

        if self.cert == '':
            frame = r'{lang_value}'
        elif self.cert == 'cf':
            frame = r'cf. {lang_value}'
        elif self.cert == 'dub':
            frame = r'{lang_value}?'
        else:
            raise ValueError('cert="' + self.cert + '" which is not a valid value.')

        return frame.format(
                lang_value=render_lang_value()
            ).replace(r'//', r'\textit{').replace(r'\\', r'}')
