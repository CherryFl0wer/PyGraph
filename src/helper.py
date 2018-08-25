"""
@name: makeGremlin
@param: vertex 
@param: state
@return: (vertex, state || None)

Any object that has a vertex property and a state property
is a gremlin by this definition.

TLDR; A gremlin represents a potential query result.
"""
def makeGremlin(vertex, state):
    return { "vertex" : vertex, "state": state or None }



"""
@name: goToVertex
@param: gremlin :: Dict
@param: vertex :: Dict
@return: (Dict -> Bool)

Change gremlin position
"""

def goToVertex(gremlin, vertex):
    return makeGremlin(vertex, gremlin["state"])


"""
@name: objectFilter
@param: vertex :: Dict
@param: filtr :: Dict
@return: Bool

Return true or false whether or not each key correspond to the filter
"""
def objectFilter(vertex, filtr):
    for key, value in filtr.items():
        if value != vertex[key]:
            return False

    return True


"""
@name: filterEdges
@param: filtr :: String
@return: (Dict -> Bool)

Return true or false whether or not the edge label / object correspond to the filter 
"""
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
