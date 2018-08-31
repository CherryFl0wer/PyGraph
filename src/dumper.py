import pickle
import time 


def saveGraph(graph):
    t = time.mktime(time.gmtime())
    name = 'graph-{0}'.format(t)
    name = name[:-2] + ".bin"

    with open(name, 'wb') as f:
        pickle.dump(graph, f)
    
    return name

def loadGraph(filename):
    graph = None
    with open(filename, 'rb') as f:
        graph = pickle.load(f)
    
    return graph