from src.pipetypes import Pipetype
import src.helper as hp 


"""
@name:   vertex
@param:  graph :: Dict
@param:  gremlin :: Dict
@param:  state :: Dict 
@param   args :: Array<Any>
@return: Dict

Create a gremlin by finding matching vertices, args contain the filters 
needed for the graph to find the different vertices
"""
def vertex(graph, gremlin, state, args):
    
    if "vertices" not in state:
        state["vertices"] = graph.findVertices(args)
    
    if len(state["vertices"]) == 0 :
        return "done"
    
    vertex = state["vertices"].pop()

    if not isinstance(gremlin, dict) or "state" not in gremlin:
        return hp.makeGremlin(vertex, False)

    return hp.makeGremlin(vertex, gremlin["state"])

"""
@name:   traversal
@param: direction :: String
@return: (
    @param:  graph :: Dict,
    @param:  gremlin :: Dict,
    @param:  state :: Dict ,
    @param   args :: Array<Any>
    -> Dict
)

Go through the graph by following the filter direction (_in or _out)
"""
def traversal(direction):

    method = "findOutEdges" if direction == "out" else "findInEdges"
    edgeList = "_in" if direction == "out" else "_out"

    def _traversal(graph, gremlin, state, args):
        
        # no gremlin that means no edge availaible
        if not gremlin and ("edges" not in state or len(state["edges"]) == 0):
            return "pull"
        
        # We have a gremlin but no edge
        if "edges" not in state or len(state["edges"]) == 0:
           
            state["gremlin"] = gremlin
            filtre = None if len(args) == 0 else args[0]
            state["edges"] = list(filter(hp.filterEdges(filtre),
                                    getattr(graph, method)(gremlin["vertex"])))

        if len(state["edges"]) == 0:
            return "pull"
        
        vertex = state["edges"].pop()[edgeList]
       
        return hp.goToVertex(state["gremlin"], vertex)

    return _traversal


"""
@name:  property
@param:  graph :: Dict,
@param:  gremlin :: Dict,
@param:  state :: Dict ,
@param:  args :: Array<Any>
@return: Dict

Get the value from a dict
"""
def property(graph, gremlin, state, args):
    if not gremlin: #No gremlin means no property
        return "pull"
    
    if len(args) == 0 or args[0] not in gremlin["vertex"]:
        return False
    
    gremlin["finish"] = gremlin["vertex"][args[0]]
    return gremlin

"""
@name:  isUnique
@param:  graph :: Dict,
@param:  gremlin :: Dict,
@param:  state :: Dict ,
@param:  args :: Array<Any>
@return: Dict

Check if vertex is unique in our query.
Set to true if never passed by this vertex otherwise pull
"""
def isUnique(graph, gremlin, state, args):
    if not gremlin or gremlin["vertex"]["_id"] in state:
        return "pull"  
    
    state[gremlin["vertex"]["_id"]] = True
    return gremlin

"""
@name:  filter
@param:  graph :: Dict,
@param:  gremlin :: Dict,
@param:  state :: Dict ,
@param:  args :: Array<Any>
@return: Dict

Filter vertex
"""
def filtering(graph, gremlin, state, args):
    if not gremlin or len(args) == 0:
        return "pull"  
    
    if isinstance(args[0], dict):
        return gremlin if hp.objectFilter(gremlin["vertex"], args[0]) else "pull"

    if callable(args[0]):
        return gremlin if args[0](gremlin["vertex"]) else "pull"
    
    return gremlin


# Add methods to pipetype availaibility


def __initPipetypes():
    Pipetype.addPipetype('vertex', vertex)  
    Pipetype.addPipetype('o', traversal('out'))
    Pipetype.addPipetype('i', traversal('in'))
    Pipetype.addPipetype('property', property)
    Pipetype.addPipetype('unique', isUnique)
