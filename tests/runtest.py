import unittest
import sys
import os

sys.path.append(os.path.abspath('./'))

from src.graph import Graph
from src.dumper import saveGraph, loadGraph
from traversal_test import TraversalTests

if __name__ == '__main__':
    print("Launching test...")

    V = [ { "_id": 1, "name": 'alice'}                                         
        , { "_id": 10, "name": 'bob', "hobbies": ["basket", "game"] } 
        ] 

    E = [ { "_out": 1, "_in": 10, "_label": 'knows'} ]
    G = Graph(V,E)

    G.addVertex({"name": "delta", "_id": 30})
    G.addVertex({ "name": 'charlie', "_id": 'charlie'}) 

    G.addEdge({"_out": 10, "_in": 30, "_label": 'parent'})
    G.addEdge({"_out": 10, "_in": 'charlie', "_label": 'knows'})
    G.addEdge({"_out": 30, "_in": 'charlie', "_label": 'unknows'})
    G.addEdge({"_out": 'charlie', "_in": 30, "_label": 'unknows'})

    G.initpipe()
    print("Graph created testing...")
    TraversalTests(G).run()

   # print("Testing pickle")
   # filename = saveGraph(G)



    
    
