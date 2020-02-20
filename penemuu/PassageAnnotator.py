import os
import spacy
from penemuu import TextPassage
from spacy.pipeline import EntityRuler
from pysbd.utils import PySBDFactory

#temporary
import en_core_web_sm

class PassageAnnotator:
    """
    Functional class to identify and link named entities in a biomedical text.

    Entities of interest are provided as a jsonl file with 1 entry per line, which is used to populate an EntityRuler object.
    """

    def __init__(self):
        self.nlp = en_core_web_sm.load()
        self.entity_ruler = None

    def add_entity_ruler_from_jsonl(self, jsonl_path):
        """
        Add an EntityRuler component to the spacy model's pipeline generated from a jsonl file.

        :param jsonl_path: jsonl file where each line contains an EntityRuler pattern, ex: {"label":"BACTERIA","pattern":"dictyoglomus thermophilum","id":"14"}
        """

        if os.path.isfile(jsonl_path):
            """
            Adding a large number (50k+) of entities to EntityRuler is extremely slow.  
            Disabling other pipeline components before loading the jsonl file addresses this:
                https://github.com/explosion/spaCy/issues/4119
            """
            disabled = self.nlp.disable_pipes("tagger", "parser", "ner")
            self.entity_ruler = EntityRuler(self.nlp)
            self.entity_ruler.from_disk(jsonl_path)
            disabled.restore()
            print("Entity ruler generated from jsonl at %s" % jsonl_path)

            self.nlp.add_pipe(self.entity_ruler, before='ner')
            self.nlp.remove_pipe('ner')
            print("Entity ruler added to spacy pipeline.")

            #Sentence boundary disambiguation
            self.nlp.add_pipe(PySBDFactory(self.nlp), before='parser')
            print("PySBDFactory added to spacy pipeline.")

    def annotate_text_with_named_entities(self, text):
        """
        Using an EntityRuler component, identify named entities and merge their component tokens.
        :param passage (str): a text passage.
        :return (Spacy.doc): a doc object that includes the identified named entities.
        """

        doc = self.nlp(text.lower())
        with doc.retokenize() as retokenizer:
            for ent in doc.ents:
                retokenizer.merge(ent)

        return doc

    def annotate_passage(self, penemuu_passage):

        passage_doc = self.annotate_text_with_named_entities(penemuu_passage.text)

        penemuu_passage.add_annotated_sentences(passage_doc)

        return penemuu_passage


