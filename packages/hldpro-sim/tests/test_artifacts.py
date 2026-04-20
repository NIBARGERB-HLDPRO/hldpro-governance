import json
import tempfile

from hldprosim.artifacts import ArtifactWriter, RunManifest


def test_artifact_writer_writes_manifest_and_outcomes():
    outcomes = [{"persona_id": "trader-momentum", "result": "buy"}, {"persona_id": "trader-momentum", "result": "sell"}]

    with tempfile.TemporaryDirectory() as tmp:
        manifest = RunManifest(
            run_id="run-001",
            provider="codex",
            model="gpt-5.4",
            persona_id="trader-momentum",
            n_runs=2,
        )
        writer = ArtifactWriter(base_dir=tmp)

        run_dir = writer.write(manifest, outcomes)

        manifest_path = run_dir / "run_manifest.json"
        outcomes_path = run_dir / "outcomes.jsonl"

        assert manifest_path.exists()
        assert outcomes_path.exists()

        manifest_json = json.loads(manifest_path.read_text())
        assert manifest_json["run_id"] == "run-001"

        lines = outcomes_path.read_text().strip().split("\n")
        assert len(lines) == 2
