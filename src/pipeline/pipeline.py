
class State:
    userInput: str
    dataPath: str
    sqlQuery: str
    metaData: str
    sqlResult : str
    visNeed : bool
    visQuery : str
    pythonCode : str
    plots : str
    results : list
class Pipeline:
    def invoke(state:State, query):
        return state
        pass
