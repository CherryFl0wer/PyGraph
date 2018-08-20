"""
@name: makeGremlin
@param: vertex 
@param: state
@return: (vertex, state || None)

Any object that has a vertex property and a state property
is a gremlin by this definition.
"""
def makeGremlin(vertex, state):
    return vertex, state or None


def goToVertex(gremlin, vertex):
    return makeGremlin(vertex, gremlin["state"])

def objectFilter(vertex, filtr):
    for key, value in filtr.items():
        if value != vertex[key]:
            return False

    return True

def filterEdges(filtr):
    def _filterEdges(edge):
        if filtr is None:
            return True
        
        if isinstance(filtr, str):
            return edge["_label"] == filtr
        
        if isinstance(filtr, list):
            return edge["_label"] in filtr
        
        return objectFilter(edge, filtr)
        
    return _filterEdges
