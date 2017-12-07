import pygraphviz as pgv
import json

index = 0


def _add_node(G, subtree, parent, left):
    global index

    node_id = index
    index += 1
    if subtree['left'] and subtree['right']:
        G.add_node(node_id, label="{} &le; {}?\nsamples = {} ({}+, {}-)\ngain = {}".format(subtree['attribute'],
                                                                                           subtree['threshold'],
                                                                                           subtree['samples'],
                                                                                           subtree['pos_samples'],
                                                                                           subtree['neg_samples'],
                                                                                           round(subtree['gain'], 4)),
                   color='#5191f7')
        if subtree['left']:
            _add_node(G, subtree['left'], node_id, True)
        if subtree['right']:
            _add_node(G, subtree['right'], node_id, False)
    else:
        # This is a leaf
        if subtree['value'] == 1:
            color = '#cdffb2'
        else:
            color = '#ffd5b2'
        G.add_node(node_id,
                   label="class_label = {}\nsamples = {} ({}+, {}-)".format(bool(subtree['value']), subtree['samples'],
                                                                            subtree['pos_samples'],
                                                                            subtree['neg_samples']),
                   color=color)

    if parent >= 0:
        G.add_edge(parent, node_id, headlabel='{}'.format(left))


def generate_dot_from_graph(tree, outputpath):
    G = pgv.AGraph(directed=True)
    G.node_attr['shape'] = 'box'

    _add_node(G, tree, -1, False)

    G.write(outputpath)


if __name__ == '__main__':
    with open('ausgabe_depth_10.json') as fp:
        tree = json.load(fp)

    generate_dot_from_graph(tree, 'output_depth_10.dot')