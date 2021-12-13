from load_save_movies import load_movies


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


def filter(condition, verts):
    by_condition = []
    for vert in verts:
        if vert.getFeature() == condition[0] and vert.getValue() == condition[1]:
            by_condition = vert.getConnections()
            break
    return by_condition


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