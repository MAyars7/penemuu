import spacy

class PassageSentence:

    def __init__(self, spacy_sent = None):
        """

        Extends a spaCy sentence (span object) to track the subject(s) and object(s) of a sentence.

        This is useful for coreferences: general terms that refer to specific terms in the previous sentence.

        :param spacy_sent: a spaCy span object containing a complete sentence.
        """

        self.spacy_sent = ''
        self.subjs = []
        self.objs = []
        self.ents = []

        if spacy_sent:

            self.spacy_sent = spacy_sent

            for token in spacy_sent:
                if token.dep_ in ['nsubj', 'csubj']:
                    self.subjs.append(token)

                elif token.dep_ in ['pobj', 'dobj', 'obj']:
                    self.objs.append(token)

                if token.ent_type_:
                    self.ents.append(token)




