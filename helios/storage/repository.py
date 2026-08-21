from helios.contracts.models import AnalysisRun


class InMemoryRunRepository:
    """Hackathon-safe adapter; replace with PostGIS without changing API contracts."""

    def __init__(self) -> None:
        self._runs: dict[str, AnalysisRun] = {}

    def save(self, run: AnalysisRun) -> AnalysisRun:
        self._runs[run.run_id] = run.model_copy(deep=True)
        return run

    def get(self, run_id: str) -> AnalysisRun | None:
        run = self._runs.get(run_id)
        return run.model_copy(deep=True) if run else None
