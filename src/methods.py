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


# Add methods to pipetype availaibility

def __initPipetypes():
    Pipetype.addPipetype('vertex', vertex)  
    Pipetype.addPipetype('out', traversal('out'))
    Pipetype.addPipetype('in', traversal('in'))
