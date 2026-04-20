from concurrent.futures import ThreadPoolExecutor, as_completed

from .engine import SimulationEngine


class Runner:
    def __init__(self, max_workers: int | None = None):
        self.max_workers = max_workers

    def run_n(self, engine: SimulationEngine, event: dict, persona_id: str, n: int) -> list[dict]:
        if self.max_workers and self.max_workers > 1:
            with ThreadPoolExecutor(max_workers=self.max_workers) as ex:
                futures = [ex.submit(engine.run, event, persona_id) for _ in range(n)]
                return [f.result() for f in as_completed(futures)]

        return [engine.run(event, persona_id) for _ in range(n)]
