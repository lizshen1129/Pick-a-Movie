import json
from graph import *


def load_graph():
    try:
        graph_file = open(GRAPH_FILE_NAME, 'r')
        graph = graph_file.read()
        graph_dict = json.loads(graph)
        graph_file.close()
        verts = []
        for key in graph_dict.keys():
            value = key.split('>>')[0]
            feature = key.split('>>')[1]
            new_vert = Vertex(value, 0, feature)
            new_vert.setNeighbors(graph_dict[key])
            verts.append(new_vert)
        g = Graph(verts)
    except:
        g = generate_graph()
    return g


def save_graph(graph):
    graph_dict = {}
    for vert in graph.getVerts():
        graph_dict[vert.getValue() + '>>' + vert.getFeature()] = vert.getConnections()

    graph_file = open(GRAPH_FILE_NAME, 'w')
    graph_to_write = json.dumps(graph_dict)
    graph_file.write(graph_to_write)
    graph_file.close()