from src.pipetypes import Pipetype
import pprint
class Query:

    def __init__(self, graph):
        self.graph = graph
        self.pipeline = []
        self.gremlins = []
        self.state = []

    def add(self, pipetype, args):
        step = (pipetype, list(args))
        self.pipeline.append(step)
        return self
    
    def run(self):
        end = len(self.pipeline) - 1 # Step' index of the pipeline
        maybe_gremlin = False 
        results = [] 
        done = -1 # tell when it's finished
        pc = end # pipeline counter

        step = None
        state = None
        pipetype = None
        self.state = (pc + 1) * [None]

        while done < end:  
            step = self.pipeline[pc] # Tuple / Pair containing pipetype and args
            self.state[pc] = self.state[pc] if isinstance(self.state[pc], dict) else {} 
            state = self.state[pc]
            pipetype = Pipetype.getPipetype(step[0]) 

            maybe_gremlin = pipetype(self.graph, maybe_gremlin, state, step[1])  
            
            if maybe_gremlin == "pull":
                maybe_gremlin = False
                if pc - 1 > done:
                    pc -= 1
                    continue
                else:
                    done = pc
            
            if maybe_gremlin == "done":
                maybe_gremlin = False
                done = pc
            
            pc += 1

            if pc > end:
                if maybe_gremlin:
                    results.append(maybe_gremlin)
                maybe_gremlin = False
                pc -= 1


        results = map(lambda gremlin: gremlin["result"] if "result" in gremlin else gremlin["vertex"], results)
        return list(results)

    
    