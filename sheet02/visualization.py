import pygraphviz as pgv

index = 0


def _add_node(G, subtree, parent):
    global index

    node_id = index
    index += 1
    if 'threshold' in subtree:
        G.add_node(node_id, label="{} &le; {}?\nsamples = {}\ngain = {}".format(subtree['attribute'], subtree['threshold'], subtree['samples'], round(subtree['gain'], 4)), color='#5191f7')
        if subtree['left']:
            _add_node(G, subtree['left'], node_id)
        if subtree['right']:
            _add_node(G, subtree['right'], node_id)
    else:
        # This is a leaf
        if subtree['value'] == 1:
            color = '#cdffb2'
        else:
            color = '#ffd5b2'
        G.add_node(node_id, label="class_label = {}\nsamples = {}".format(bool(subtree['value']), subtree['samples']), color=color)

    if parent >= 0:
        G.add_edge(parent, node_id)


def generate_dot_from_graph(tree, outputpath):
    G = pgv.AGraph()
    G.node_attr['shape'] = 'box'

    _add_node(G, tree, -1)

    G.write(outputpath)
