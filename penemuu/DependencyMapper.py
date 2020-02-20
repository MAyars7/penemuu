class DependencyMapper:

    def __init__(self):
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

        self.nlp = en_core_web_sm.load()

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