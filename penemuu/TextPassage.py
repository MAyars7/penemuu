class TextPassage:

    def __init__(self, medline_record=None):
        """
        Object containing a biomedical text split into categorical sections.

        If a medline record is provided, title and abstract will be extracted to populate attributes.  Other formats to be added.

        :param medline_record (medline): a biomedical text in medline format.

        title (str): The title of a biomedical text.
        abstract (str): The abstract of a biomedical text.
        passage (str): The combined title and abstract.
        """

        self.title = ''
        self.abstract = ''
        self.passage = ''

        if medline_record:
            self.title = medline_record.get('TI', '')
            self.abstract = medline_record.get('AB', '')
            self.passage = ' '.join([self.title, self.abstract])

        self.ents_by_label = {}

    def add_text(self, text_passage):
        """
        Populate passage attribute with a string.

        :param text_passage (str): biomedical text of one or more sentences.
        """

        self.passage = text_passage

    def extract_title_and_abstract_from_medline(self, medline_record):
        """
        Populate attributes with title and abstract extracted from a medline record.

        :param medline_record (medline): biomedical text in medline format.
        """

        self.title = medline_record.get('TI', '')
        self.abstract = medline_record.get('AB', '')
        self.passage = ' '.join(self.title, self.abstract)