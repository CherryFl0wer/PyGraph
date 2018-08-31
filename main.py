from src.graph import Graph
from src.dumper import loadGraph
import sys


if __name__ == '__main__':

    graph = loadGraph(sys.argv[1]).initpipe()
    print(graph.v(1).o().run())

    
