class Pipetype:

    pipetypes = {}

    @staticmethod
    def addPipetype(fct_name, fct):
        Pipetype.pipetypes[fct_name] = fct

        def add_query(self, *args):
            return self.add(fct_name, args)

        from src.query import Query
        setattr(Query, fct_name, add_query)

    @staticmethod
    def getPipetype(fct_name):

        def err(graph, state, maybe):
            return maybe or "pull"

        if fct_name not in Pipetype.pipetypes:
            print("pipetypes not existing") #TODO Error
            return err
        
        return Pipetype.pipetypes[fct_name]
        