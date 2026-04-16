import time


class BaseAnalyser:
    """Base class for IFC analysis."""

    def run(self, file_path):
        """Return a dict of results for the given IFC file path."""
        raise NotImplementedError

    def execute(self, file_path):
        started = time.perf_counter()
        result = self.run(file_path)
        duration_ms = int((time.perf_counter() - started) * 1000)
        return result, duration_ms

    @staticmethod
    def with_meta(result, analysis_type):
        payload = dict(result or {})
        payload.setdefault("analysis_type", analysis_type)
        return payload
