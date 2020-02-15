import penemuu
from Bio import Medline

class PassageCorpus:

    def __init__(self):
        """
        text_passages (list): TextPassage objects, each containing a biomedical text.
        """

        self.text_passages = []
        #self.ann_text_passages = []

    def add_text(self, text_passage):
        """
        Add a text passage in string format to the text_passages attribute.

        :param text_passage (str): a biomedical text passage of one or more sentences.
        """

        self.text_passages.append(text_passage)

    def add_medline_records_from_file(self, medline_record_file):
        """
        Add all medline records in a file to the text_passages attribute.

        :param medline_record_file (str): file containing biomedical texts in medline record format.
        """

        with open(medline_record_file) as handle:
            records = Medline.parse(handle)
            for record in records:
                self.text_passages.append(penemuu.TextPassage(record))






