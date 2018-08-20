from src.pipetypes import Pipetype

class Query:

    def __init__(self, graph):
        self.graph = graph
        self.pipeline = []
        self.gremlins = []
        self.state = []

    def add(self, pipetype, args):
        step = (pipetype, args)
        self.pipeline.append(step)
        return self
    
    def run(self):
        end = len(self.pipeline) - 1 # Step' index of the pipeline
        maybe_gremlin = False 
        results = [] 
        done = -1 # tell when it's finished
        pc = end # pipeline counter

        print(self.pipeline)
        step = None
        state = None
        pipetype = None

        while done < end: 
            ts = list(self.state)
            step = self.pipeline[pc] # Tuple / Pair containing pipetype and args
            state = ts[pc] if isinstance(ts[pc], dict) else {} 
            pipetype = Pipetype.getPipetype(step[0]) 

            maybe_gremlin = pipetype(self.graph, step[1], maybe_gremlin, state)

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
        
        results = map(lambda gremlin: gremlin["result"] if gremlin["result"] is not None else gremlin["vertex"], results)
        return results

    
    