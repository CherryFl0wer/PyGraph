from src.pipetypes import Pipetype
import src.helper as hp 

def vertex(graph, gremlin, state, *args):
    if "vertices" not in state:
        state["vertices"] = graph.findVertices(args)
    
    if len(state["vertices"]) == 0:
        return "done"
    
    vertex = state["vertices"].pop()
    return hp.makeGremlin(vertex, gremlin["state"])


def traversal(direction):

    method = "findOutEdges" if direction == "out" else "findInEdges"
    edgeList = "_out" if direction == "out" else "_in"

    def _traversal(graph, gremlin, state, *args):
        
        if not gremlin and ("edges" not in state or len(state["edges"]) == 0):
            return "pull"
        
        if state["edge"] is None or len(state["edge"]) == 0:
            state["gremlin"] = gremlin
            state["edges"] = filter(lambda x: hp.filterEdges(args[0]),
                                    getattr(graph, method)(gremlin["vertex"]))

        if len(state["edges"]) == 0:
            return "pull"
        
        vertex = state["edges"].pop()[edgeList]
        return hp.goToVertex(state["gremlin"], vertex)

    return _traversal


def __initPipetypes():
    Pipetype.addPipetype('vertex', vertex)  
    Pipetype.addPipetype('out', traversal('out'))
    Pipetype.addPipetype('in', traversal('in'))
