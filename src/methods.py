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

"""
@name:  take
@param:  graph :: Dict,
@param:  gremlin :: Dict,
@param:  state :: Dict ,
@param:  args :: Array<Any>
@return: Dict

Return element args[0] by args[0]
args[0] need to be an int
"""
def take(graph, gremlin, state, args): 
    if len(args) == 0:
        return "pull"
        
    if "taken" not in state:
        state["taken"] = 0

    if state["taken"] == args[0]:
        state["taken"] = 0
        return "done"

    if not gremlin:
        return "pull"

    state["taken"] += 1
    return gremlin

"""
@name:  like
@param:  graph :: Dict,
@param:  gremlin :: Dict,
@param:  state :: Dict ,
@param:  args :: Array<Any>
@return: Dict

label the current vertices
"""
def like(self, graph, gremlin, state, args):
  if not gremlin: 
      return "pull" 
                                
  gremlin["state"]["as"] = gremlin["state"]["as"] or {}                  
  gremlin["state"]["as"][args[0]] = gremlin["vertex"]                 
  return gremlin

"""
@name:  merge
@param:  graph :: Dict,
@param:  gremlin :: Dict,
@param:  state :: Dict ,
@param:  args :: Array<Any>
@return: Dict

Copie 
"""
def merge(self, graph, gremlin, state, args):
    if not gremlin or "vertices" not in state: 
        return "pull" 

    if "vertices" not in state or len(state["vertices"]) == 0:
        asname = gremlin["state"] if "state" in gremlin else {}
        asname = asname["as"] if "as" in asname else {}
        state["vertices"] = list(filter(lambda x: True if x is not None else False, 
                                    map(lambda renamed: asname[renamed], args)
                                )) # Rename the vertex by copying the vertex from the state 'as' 

    
    if len(state["vertices"]) == 0:
        return "pull"
    
    vertex = state["vertices"].pop()
    return hp.makeGremlin(vertex, gremlin["state"])

# Add methods to pipetype availaibility


def __initPipetypes():
    Pipetype.addPipetype('vertex', vertex)  # Go to a vertex
    Pipetype.addPipetype('o', traversal('out')) # Out edge
    Pipetype.addPipetype('i', traversal('in')) # In edge
    Pipetype.addPipetype('property', property) # Get specific value from a dict
    Pipetype.addPipetype('unique', isUnique) # Filter uniqueness
    Pipetype.addPipetype('filter', filtering)   # Filter your own method
    Pipetype.addPipetype('take', take)  # Take element x by x
    Pipetype.addPipetype('like', like) # Renamer
    Pipetype.addPipetype('merge', merge) # Merging renamer
