from src.query import Query
from src.helper import objectFilter
from src.methods import __initPipetypes as pipeinit

class Graph:

    def __init__(self, V, E):
        self.edges = []
        self.vertices = []
        self.lookupIndex = {}
        self.uniqueID = 1

        if isinstance(V, list) and isinstance(E, list):
            self.addVertices(V)
            self.addEdges(E)


    def v(self, *args):
        pipeinit()
        query = Query(self)
        query.add('vertex', list(args))
        return query
        
    def addVertices(self, V):
        for vertex in V:
            self.addVertex(vertex)
           

    def addVertex(self, vertex):
        
        if "_id" not in vertex: # Create unique index
            vertex["_id"] = self.uniqueID
            self.uniqueID += 1
        elif self.findVertexByID(vertex["_id"]) is not None: 
            raise Exception("ID already existing in graph") 
            
        self.vertices.append(vertex)
        self.lookupIndex[vertex["_id"]] = vertex # Fast access to vertex

        vertex["_out"] = []
        vertex["_in"] = []
    
    def addEdges(self, E):
        for edge in E:
            self.addEdge(edge)
    
    def addEdge(self, edge):
        edge["_in"] = self.findVertexByID(edge["_in"])
        edge["_out"] = self.findVertexByID(edge["_out"])

        if "_in" not in edge or "_out" not in edge:
            raise Exception("Impossible to create edge %d -> %d".format(edge["_in"], edge["_out"])) # Better managing error TODO
            
        edge["_in"]["_in"].append(edge)
        edge["_out"]["_out"].append(edge)

        self.edges.append(edge)
    
    def findVertexByID(self, id):
        return  None if id not in self.lookupIndex else self.lookupIndex[id]
    
    def findVertexByIDS(self, ids):
        
        if len(ids) == 1:
            maybe_vertex = self.findVertexByID(ids[0])
            return [maybe_vertex] if maybe_vertex is not None else []
        
        return filter(lambda x: x is not None, map(self.findVertexByID, ids))

    def findVertices(self, args):
        if isinstance(args[0], dict):
            return self.searchVertices(args[0])
        elif len(args) == 0:
            return list(self.vertices)
        else:
            return self.findVertexByIDS(args)
    
    def searchVertices(self, filtr):
        return filter(lambda vertex: objectFilter(vertex, filtr) ,self.vertices)
    
    def findOutEdges(self, vertex):
        return vertex["_out"]
    
    def findInEdges(self, vertex):
        return vertex["_in"]
    