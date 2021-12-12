import json


class Vertex:
    def __init__(self, value, movie_id, feature):
        self.value = value
        self.feature = feature
        self.connectedTo = [movie_id]

    def addNeighbor(self, movie_id):
        self.connectedTo.append(movie_id)

    def setNeighbors(self, neighbors):
        self.connectedTo = neighbors

    def getValue(self):
        return self.value

    def getFeature(self):
        return self.feature

    def getConnections(self):
        return self.connectedTo


class Graph():
    def __init__(self, verts=[]):
        self.vertList = verts

    def addVert(self, vert):
        self.vertList.append(vert)

    def checkVert(self, value, movie_id, feature):
        for existingVert in self.vertList:
            if value == existingVert.getValue() and feature == existingVert.getFeature():
                if movie_id not in existingVert.getConnections():
                    # The vertex already exists, update neighbor
                    existingVert.addNeighbor(movie_id)
                return
        # The vertex doesn't exist, add this vertex
        self.addVert(Vertex(value, movie_id, feature))

    def getVerts(self):
        return self.vertList


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


def load_movies():
    try:
        movies_file = open(MOVIES_DICT_NAME, 'r')
        movies = movies_file.read()
        movies_dict = json.loads(movies)

        movies_file.close()
    except:
        movies_dict = {}
    return movies_dict


def filter(condition, verts):
    by_condition = []
    for vert in verts:
        if vert.getFeature() == condition[0] and vert.getValue() == condition[1]:
            by_condition = vert.getConnections()
            break
    return by_condition


def result_dict(movie_ids):
    if movie_ids is None:
        return
    result = {'Title': [], 'Year': [], 'Classification': [], 'Length': [], 'Rating': [], 'Genres': [], 'Directors': [],
              'Writers': [], 'Stars': [], 'URL': [], 'img': []}
    for movie_id in movie_ids:
        movie_id = int(movie_id)
        for key in MOVIES_DICT.keys():
            result[key].append(MOVIES_DICT[key][movie_id])
    return result


def generate_length_verts(movies_graph, feature, movie_id):
    if 'h' not in MOVIES_DICT[feature][movie_id]:
        movies_graph.checkVert('Less than 1 hour', movie_id, feature)
    elif MOVIES_DICT[feature][movie_id][0] == '1':
        movies_graph.checkVert('Less than 2 hours', movie_id, feature)
    elif MOVIES_DICT[feature][movie_id][0] == '2':
        movies_graph.checkVert('Less than 3 hours', movie_id, feature)
    else:
        movies_graph.checkVert('3 hours and above', movie_id, feature)


def generate_rating_verts(movies_graph, feature, movie_id):
    if MOVIES_DICT[feature][movie_id] >= 9:
        movies_graph.checkVert('9-10', movie_id, feature)
    elif MOVIES_DICT[feature][movie_id] >= 8:
        movies_graph.checkVert('8-9', movie_id, feature)
    else:
        movies_graph.checkVert('Below 8', movie_id, feature)


def generate_graph():
    movies_graph = Graph()
    for movie_id in range(250):
        for feature in MOVIES_DICT.keys():
            if feature in ['Title', 'URL', 'img']:
                continue
            elif feature == 'Length':
                generate_length_verts(movies_graph, feature, movie_id)
            elif feature == 'Rating':
                generate_rating_verts(movies_graph, feature, movie_id)
            elif feature in ['Genres', 'Directors', 'Writers', 'Stars']:
                for per in MOVIES_DICT[feature][movie_id]:
                    movies_graph.checkVert(per, movie_id, feature)
            else:
                movies_graph.checkVert(MOVIES_DICT[feature][movie_id], movie_id, feature)
    return movies_graph


MOVIES_DICT_NAME = 'movies.json'
MOVIES_LIST_LENGTH = 250
MOVIES_DICT = load_movies()
GRAPH_FILE_NAME = 'graph.json'


'''

# Generate the graph and save it to local file, 'graph.json'.

g = load_graph()
save_graph(g)

'''