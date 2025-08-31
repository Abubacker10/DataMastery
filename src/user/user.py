from collections import defaultdict
from typing import List, Dict, Any, Optional
from  pipeline.pipeline import Pipeline 


class QueryHistory:
    """Handles storage and retrieval of query execution history."""

    def __init__(self):
        self._history: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    def add_record(self, dataset: str, query: str, result: Any) -> None:
        self._history[dataset].append({query: result})

    def get_records(self, dataset: Optional[str] = None) -> Dict[str, List[Dict[str, Any]]]:
        if dataset:
            return {dataset: self._history.get(dataset, [])}
        return self._history

    def clear_records(self, dataset: Optional[str] = None) -> None:
        if dataset:
            self._history[dataset].clear()
        else:
            self._history.clear()


class PipelineInterface:
    """Abstract pipeline interface for Dependency Inversion Principle."""

    def run(self, query: str, dataset: str) -> Dict[str, Any]:
        raise NotImplementedError


class DefaultPipeline(PipelineInterface):
    """Concrete implementation of a pipeline using the existing invoke function."""

    def run(self, query: str, dataset: str) -> Dict[str, Any]:
        return Pipeline.invoke(query, dataset)


class User:
    """Represents a user interacting with the SQL pipeline system."""

    def __init__(self, username: str, pipeline: PipelineInterface = None):
        self.username = username
        self.queries: List[str] = []
        self.datasets: List[str] = []
        self.history = QueryHistory()
        self.pipeline = pipeline or DefaultPipeline()

    def execute_query(self, query: str, dataset: str) -> Any:
        print(f"[{self.username}] Processing query `{query}` on dataset `{dataset}`")
        self.queries.append(query)
        self.datasets.append(dataset)

        state = self.pipeline.run(query, dataset)
        result = state.get("results", None)

        self.history.add_record(dataset, query, result)
        return result

    def get_history(self, dataset: Optional[str] = None) -> Dict[str, List[Dict[str, Any]]]:
        return self.history.get_records(dataset)

    def clear_history(self, dataset: Optional[str] = None) -> None:
        self.history.clear_records(dataset)

userAbu = User('abu')
print(userAbu.execute_query('display plots','data.csv'))

