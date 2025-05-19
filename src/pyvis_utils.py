from pyvis.network import Network
from rdflib import Graph, term
import os


def graph_to_pyvis_net(graph: Graph, path: str, file_name: str, display: bool = False):
    """
    :param graph: grafo di rdflib che si vuole visualizzare
    :param path: path in cui salvare il file html
    :param file_name: nome del file html
    :param display: se True, apre il file html nel browser
    :return:


    :param graph: rdflib graph to be visualized
    :param path: path where the HTML file will be saved
    :param file_name: name of the HTML file
    :param display: if True, opens the HTML file in the browser
    :return: 
    """
    if not os.path.exists(path):
        os.makedirs(path)
    net = Network()
    net.toggle_physics(False)
    net.show_buttons()
    # necessario prima configure, seguito da opzioni
    options = '''
            var options = {
                "configure": {
                    "enabled": true,
                    "filter": ["physics"]
                },
                "physics": {
                        "barnesHut": {
                        "gravitationalConstant": -30000,
                        "avoidOverlap": 1
                        }
                }
            }
        '''
    net.set_options(options)

    nodes = set()
    edges = set()
    blank_nodes_mapping = {}
    for s, p, o in graph:
        if isinstance(s, term.BNode):
            if s not in blank_nodes_mapping:
                blank_nodes_mapping[s] = f"blank_node_{len(blank_nodes_mapping)}"
            s = blank_nodes_mapping[s]
        else:
            s = str(s)
        if isinstance(o, term.BNode):
            if o not in blank_nodes_mapping:
                blank_nodes_mapping[o] = f"blank_node_{len(blank_nodes_mapping)}"
            o = blank_nodes_mapping[o]
        else:
            o = str(o)
        nodes.add(s)
        nodes.add(o)
        edges.add((s, o, p))

    for node in nodes:
        net.add_node(node, label=node)
    for edge in edges:
        net.add_edge(edge[0], edge[1], label=edge[2])
    if path[-1] == "/":
        path = path[:-1]
    if display:
        net.show(os.path.abspath(path) + "/" + file_name + ".html", notebook=False)
    else:
        net.save_graph(path + "/" + file_name + ".html")
