from src.pipetypes import Pipetype
import pprint

class Query:

    """
    @name: __init__
    @param: graph :: Dict 

    Init query interpreter, initialize 
        - @attribute graph, which hold the current graph
        - @attribute pipeline, contain every 'action' wanted
        - @attribute gremlins,  *
        - @attribute state, *
    """
    def __init__(self, graph):
        self.graph = graph
        self.pipeline = []
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

        if len(self.state) != pc + 1:
            self.state = (pc + 1) * [None] # init state

        while done < end:  
            step = self.pipeline[pc] # Pair containing pipetype and args
            self.state[pc] = self.state[pc] if isinstance(self.state[pc], dict) else {} 
            state = self.state[pc]
            pipetype = Pipetype.getPipetype(step[0]) 

            maybe_gremlin = pipetype(self.graph, maybe_gremlin, state, step[1])  
            

            if maybe_gremlin == "pull": # we don't have enough information we move forward (to the right)
                maybe_gremlin = False
                if pc - 1 > done:
                    pc -= 1
                    continue
                else: 
                    done = pc
            
            if maybe_gremlin == "done": # Move pc to the left
                maybe_gremlin = False
                done = pc
            
            pc += 1
            if pc > end:
                if maybe_gremlin:
                    results.append(maybe_gremlin)
                maybe_gremlin = False
                pc -= 1
                
        results = list(map(lambda gremlin: gremlin["finish"] if "finish" in gremlin else gremlin["vertex"], results))
  
        return results

    
    