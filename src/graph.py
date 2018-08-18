class Graph:

    def __init__(self, V, E):
        self.edges = []
        self.vertices = []
        self.lookupIndex = {}
        self.uniqueID = 1

        if isinstance(V, list) and isinstance(E, list):
            self.addVertices(V)
            self.addEdges(E)

    
    def addVertices(self, V):
        for vertex in V:
            if vertex._id is None:
                vertex._id = self.uniqueID
                self.uniqueID += 1
            elif self.findVertexByID(vertex._id) is not None:
                raise Exception("ID already existing in graph") 
            
            self.vertices.append(vertex)
            self.lookupIndex[vertex._id] = vertex

            vertex._out = []
            vertex._in = []

    
    def addEdges(self, E):
        for edge in E:
            edge._in = self.findVertexByID(edge._in)
            edge._out = self.findVertexByID(edge._out)

            if edge._in is None or edge._out is None:
                raise Exception("Impossible to create edge %d -> %d".format(edge._in, edge._out))
            
            edge._in._in.append(edge)
            edge._out._out.append(edge)

            self.edges.append(edge)
    
    def findVertexByID(self, id):
        return  None if self.lookupIndex[id] is None else self.lookupIndex[id]

    
