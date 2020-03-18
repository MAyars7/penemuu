import spacy
import en_core_web_sm

class DependencyMapper:

    def __init__(self, spacy_model=None):
        """
        Uses spaCy dependency parser to extract relationships between named entities in a sentence.

        The path between entities and their lowest common ancestor (lca) token (usually a verb) are traversed, checking for children with dependency 'neg' (not, no, etc.).

        If the path between both entities and their lca has no negation and the inclusive path from the lca to root verb of the sentence is not negated,
        the relationship is considered positive.

        To-do:
            -Add heuristic for handling coordinating conjunctions (but).
            -Change path as a list to a block of preposition/passive object dependencies as a relational phrase.
            -Test incorporation of subject/object recognition- should behavior change if entities are subj:obj vs. obj:obj ?
            -Test incorporation of direction root:entity:lca:entity vs. root:lca:entity:entity etc.
        """
        if spacy_model == None:
            self.nlp = en_core_web_sm.load()
        else:
            self.nlp = spacy_model


    def get_dep_path_to_lca(self, sent, ent_token, lca_node):

        polarity = 1
        current_node = ent_token
        nodes_in_path = []
        while current_node not in [lca_node, sent.root]:
            for child in current_node.children:
                if child.dep_ == 'NEG':
                    polarity = polarity * -1

            print(current_node, current_node.dep_, current_node.pos_)
            nodes_in_path.append(current_node)
            current_node = current_node.head

        if polarity == 1:
            return nodes_in_path
        else:
            return 0

    def get_dep_path_between_entities(self, sent, ent_1, ent_2):

        lca_node_idx = penemuu.TestFunctions.get_lca_idx_of_ent_pair(sent, (ent_1, ent_2))
        lca_node = sent[lca_node_idx]

        ent_1_path_to_lca = get_dep_path_to_lca(sent, ent_1, lca_node)
        ent_2_path_to_lca = get_dep_path_to_lca(sent, ent_2, lca_node)

        result = {
            'ent_1_path_to_lca': ent_1_path_to_lca,
            'ent_2_path_to_lca': ent_2_path_to_lca,
            'lca_node_path_to_root': [],
            'polarity': 1,
        }
        if ent_1_path_to_lca != 0 and ent_2_path_to_lca != 0:
            current_node = lca_node
            while current_node != sent.root:
                for child in current_node.children:
                    if child.dep_ == 'NEG':
                        result['polarity'] = result['polarity'] * -1

                current_node = current_node.head

        return result

    def get_entity_pairs(self, doc, ent_label1, ent_label2):
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

    def get_sentence_components(self, sentence):
        """
        :param sentence: spacy span
        :return: subjs, objs : lists of subjects and objects (as spaCy tokens) contained in sentence.
        """
        subjs = []
        objs = []

        for word in sentence:
            if word.dep_ in ['nsubj', 'nsubjpass', 'csubj']:
                subjs.append(word)
            if word.dep_ in ['pobj', 'obj', 'iobj']:
                objs.append(word)

        return subjs, objs

    def get_component_breakdown_from_sentences(self, sentences, ent_type_1, ent_type_2):
        """
        Searches the subjects and objects of each sentence for specified entity types, and returns a breakdown of groups they belong to:
            -subjects include entity type 1
            -objects include entity type 1
            -subjects include entity type 2
            -objects include entity type 2
            -subjects include entity type 1 and objects include entity type 2
            -subjects include entity type 2 and objects include entity type 1

        :param sentences (list): spaCy sentences (spans)
        :param ent_type_1 (str): name of entity type to search for
        :param ent_type_2 (str): name of entity type to search for
        :return (dict): breakdown of groups that sentences belong to.
        """
        component_breakdown_dict = {
            'sentences': sentences,
            '%s_subj_sents' % ent_type_1.lower(): set([]),
            '%s_obj_sents' % ent_type_1.lower(): set([]),
            '%s_subj_sents' % ent_type_2.lower(): set([]),
            '%s_obj_sents' % ent_type_2.lower(): set([])
        }
        idx = 0
        for sentence in sentences:
            subjs, objs = self.get_sentence_components(sentence)
            ent_pairs = self.get_entity_pairs(sentence, ent_type_1, ent_type_2)

            for ent_pair in ent_pairs:
                if ent_pair[0] in subjs:
                    component_breakdown_dict['%s_subj_sents' % ent_type_1.lower()].add(idx)
                if ent_pair[0] in objs:
                    component_breakdown_dict['%s_obj_sents' % ent_type_1.lower()].add(idx)
                if ent_pair[1] in subjs:
                    component_breakdown_dict['%s_subj_sents' % ent_type_2.lower()].add(idx)
                if ent_pair[1] in objs:
                    component_breakdown_dict['%s_obj_sents' % ent_type_2.lower()].add(idx)
            idx += 1

        type_1_subj_type_2_obj_sents = set.intersection(component_breakdown_dict['%s_subj_sents' % ent_type_1.lower()],
                                                        component_breakdown_dict['%s_obj_sents' % ent_type_2.lower()])
        type_2_subj_type_1_obj_sents = set.intersection(component_breakdown_dict['%s_obj_sents' % ent_type_1.lower()],
                                                        component_breakdown_dict['%s_subj_sents' % ent_type_2.lower()])

        component_breakdown_dict[
            '%s_subj_%s_obj_sents' % (ent_type_1.lower(), ent_type_2.lower())] = type_1_subj_type_2_obj_sents
        component_breakdown_dict[
            '%s_subj_%s_obj_sents' % (ent_type_2.lower(), ent_type_1.lower())] = type_2_subj_type_1_obj_sents

        return component_breakdown_dict


    def get_component_breakdown_counts(self, component_breakdown_dict, percentage_flag=False):
        """
        :param component_breakdown_dict (dict): Breakdown of sentences belonging to different categories returned by get_component_breakdown_from_sentences()
        :param percentage_flag (bool): If True, return groups counts as percentage of total.  Else return raw counts.
        :return (dict): raw counts or percentages of sentences in component_breakdown_dict belonging to each group.
        """

        component_breakdown_counts_dict = {}
        for key, value in component_breakdown_dict.items():

            if percentage_flag:
                component_breakdown_counts_dict[key] = float(
                    len(component_breakdown_dict[key]) / len(component_breakdown_dict['sentences']))
            else:
                component_breakdown_counts_dict[key] = len(value)

        return component_breakdown_counts_dict