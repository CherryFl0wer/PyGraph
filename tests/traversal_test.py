import unittest
import inspect

G = None

class TraversalTests():
    
    def __init__(self, graph):
        self.methods = inspect.getmembers(self, predicate=inspect.ismethod)
        self.graph = graph
    
    def run(self):
        print("\n\tLooking at {0}'s test file\n ".format(__name__))
        for method in self.methods:
            if method[0].endswith('_test'):
                print("==> {0} ".format(method[0]), end='')
                method[1]()
                print("VALID")
    

    def out_1_test(self):
        res = self.graph.v(1).o().run()
        expectedName = "bob"
        assert expectedName == res[0]["name"], "NOT VALID"
    
    def in_1_test(self):
        res = self.graph.v(10).i().run()
        expectedName = "alice"
        assert expectedName == res[0]["name"], "NOT VALID"