from .Sense import Sense


class PartOfSpeech(object):
    type = 'pos'

    def __init__(self):
        super().__init__()
        self.senses = [Sense()]
        self.pos = ''

    def __repr__(self):
        return "\t{pos}{children}".format(
            pos=self.pos,
            children=''.join([str(x) for x in self.senses]),
        )

    def render(self, settings={}):
        def render_senses():
            return r'\enskip‖\enskip'.join([x.render() for x in self.senses])

        return r'\hwpos<{pos}><{children}>'.format(
            pos=self.pos,
            children=render_senses(),
        )
