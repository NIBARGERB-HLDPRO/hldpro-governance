from concurrent.futures import Future
from unittest.mock import MagicMock, patch

from hldprosim.runner import Runner


def test_runner_run_n_returns_requested_count_without_threads():
    engine = MagicMock()
    engine.run.side_effect = [{"i": 1}, {"i": 2}, {"i": 3}]

    runner = Runner(max_workers=1)
    outcomes = runner.run_n(engine, {"headline": "Tesla"}, "trader-momentum", 3)

    assert len(outcomes) == 3


def test_runner_run_n_uses_threadpool_when_configured():
    engine = MagicMock()
    f1 = Future(); f1.set_result({"i": 1})
    f2 = Future(); f2.set_result({"i": 2})

    with patch("hldprosim.runner.ThreadPoolExecutor") as mock_tpe:
        executor = MagicMock()
        executor.submit.side_effect = [f1, f2]
        mock_tpe.return_value.__enter__.return_value = executor

        runner = Runner(max_workers=2)
        outcomes = runner.run_n(engine, {"headline": "TSLA"}, "trader-momentum", 2)

        assert len(outcomes) == 2
        assert executor.submit.call_count == 2
        mock_tpe.assert_called_once_with(max_workers=2)
