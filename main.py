from src.graph import Graph
from src.methods import __initPipetypes
import pprint

__initPipetypes()

if __name__ == '__main__':

    V = [ { "_id": 1, "name": 'alice'}                                         
        , { "_id": 10, "name": 'bob', "hobbies": ["basket", "game"] } 
        ] 

    E = [ { "_out": 1, "_in": 10, "_label": 'knows'} ]
    g = Graph(V,E)

    g.addVertex({"name": "delta", "_id": 30})
    g.addVertex({ "name": 'charlie', "_id": 'charlie'}) 

    g.addEdge({"_out": 10, "_in": 30, "_label": 'parent'})
    g.addEdge({"_out": 10, "_in": 'charlie', "_label": 'knows'})

    res = g.v(1).out("knows").out().run()
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(res)