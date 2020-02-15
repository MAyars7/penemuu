from collections import Counter
from itertools import product

def get_single_sentences_with_entities_by_labels(passage_corpus, passage_annotator, labels, outfile=''):
    """
    Scans a PassageCorpus object for sentences containing at least 1 entity of each specified label, then writes all sentences to a file.

    This function is used to generate a body of sentences for testing dependency-based relation extraction.

    :param passage_corpus (penemuu.PassageCorpus): Object containing a list of biomedical texts (penemuu.TextPassage objects).
    :param passage_annotator (penemuu.PassageAnnotator): Identifies entities in a biomedical text.
    :param labels (list): entity labels that must be found in a sentence for it to be included.  Ex: ['BACTERIA', 'HABITAT']
    :opt param outfile (str): If provided, function will write list of sentences here.
    :return (list): sentences containing one or more entities of all specified labels.
    """
    sents_with_ents_of_interest = []

    for text_passage in passage_corpus.text_passages:

        annotated_doc = passage_annotator.annotate_passage_with_named_entities(text_passage.abstract)

        for annotated_sent in annotated_doc.sents:
            label_ents_present = []

            for label in labels:
                label_ents_present.append([i for i in filter(lambda w: w.ent_type_ == label, annotated_sent)])

            if all(label_ents_present):
                sents_with_ents_of_interest.append(annotated_sent)

    if outfile:
        with open(outfile, 'w') as f:
            for sent in sents_with_ents_of_interest:
                f.write('%s\n' % sent.text)

    return sents_with_ents_of_interest

def get_entity_pairs(doc, ent_label1, ent_label2):
    """
    Generates two lists of named entities belonging to a spaCy doc and returns a list of all cross-list pairs.

    This function is used to identify all possible relations between two sets of entities within a document (e.g. bacteria and habitat).

    :param doc (spaCy doc): A text passage processed by a spaCy pipeline to search for entities.
    :param ent_label1 (string): An entity type to search doc for (ex: BACTERIA).
    :param ent_label2 (string): A second entity type to search doc for.
    :return (list): tuples where item 1 is a named entity with ent_label1 and item 2 is a named entity with ent_label2.
    """
    ent_label1_ents = [i for i in filter(lambda w: w.ent_type_ == ent_label1, doc)]
    ent_label2_ents = [i for i in filter(lambda w: w.ent_type_ == ent_label2, doc)]
    entity_pairs = [i for i in product(ent_label1_ents, ent_label2_ents)]

    return entity_pairs

def get_entity_token_idx(sent, ent_token):
    """
    Get the index of a spaCy token within a spaCy sent.

    :param sent (spaCy sent): Sentence from a spaCy doc.sents generator.
    :param ent_token (spaCy token): Token belonging to sent.
    :return (int): Index of token within sent.
    """
    return ent_token.i - sent.start

def get_lca_idx_of_ent_pair(doc, ent_pair):
    """
    Gets the index of the lowest common ancestor (LCA) token within a spaCy doc for a given pair of entities.

    The doc.get_lca_matrix() function produces a pairwise array of all tokens in a doc, where a given value is the index of the lowest common token shared by the
    row and column tokens via dependencies.

    :param doc (spaCy doc): Text passage processed with a spaCy pipeline.
    :param ent_pair (tuple): Two tokens belonging to doc.
    :return (int): Index of the LCA token for ent_pair argument.
    """
    lca_matrix = doc.get_lca_matrix()
    ent1_token, ent2_token = ent_pair
    ent1_idx = get_entity_token_idx(doc, ent1_token)
    ent2_idx = get_entity_token_idx(doc, ent2_token)
    lca_idx = lca_matrix[ent1_idx, ent2_idx]

    return lca_idx