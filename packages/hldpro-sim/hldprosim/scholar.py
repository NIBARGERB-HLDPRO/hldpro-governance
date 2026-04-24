from __future__ import annotations

from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path
from typing import Any

import yaml


class ScholarValidationError(ValueError):
    """Raised when packaged Scholar artifacts are internally inconsistent."""


POINTER_REQUIRED_FIELDS = {
    "capability_id",
    "version",
    "perspectives",
}

POINTER_ENTRY_REQUIRED_FIELDS = {
    "id",
    "name",
    "path",
    "contract_version",
    "input_schema_ref",
    "output_schema_ref",
    "lineage_summary",
    "status",
}

PERSPECTIVE_FRONTMATTER_REQUIRED_FIELDS = {
    "id",
    "name",
    "contract_version",
    "input_schema_ref",
    "output_schema_ref",
    "lineage_summary",
}


@dataclass(frozen=True)
class ScholarPerspective:
    perspective_id: str
    name: str
    path: Path
    contract_version: str
    input_schema_ref: str
    output_schema_ref: str
    lineage_summary: str
    status: str
    content: str
    frontmatter: dict[str, Any]


@dataclass(frozen=True)
class ScholarCatalog:
    capability_id: str
    version: str
    pointer_path: Path
    bundles: dict[str, list[str]]
    perspectives: dict[str, ScholarPerspective]

    def select(
        self,
        perspective_ids: list[str] | None = None,
        bundle_id: str | None = None,
    ) -> list[ScholarPerspective]:
        if perspective_ids and bundle_id:
            raise ScholarValidationError("Specify perspective_ids or bundle_id, not both")

        selected_ids = perspective_ids
        if bundle_id is not None:
            try:
                selected_ids = self.bundles[bundle_id]
            except KeyError as exc:
                raise ScholarValidationError(f"Unknown Scholar bundle '{bundle_id}'") from exc

        if not selected_ids:
            selected_ids = list(self.perspectives.keys())

        selected: list[ScholarPerspective] = []
        for perspective_id in selected_ids:
            try:
                selected.append(self.perspectives[perspective_id])
            except KeyError as exc:
                raise ScholarValidationError(
                    f"Unknown Scholar perspective '{perspective_id}'"
                ) from exc
        return selected

    def build_invocation_context(
        self,
        perspective_ids: list[str] | None = None,
        bundle_id: str | None = None,
    ) -> dict[str, Any]:
        selected = self.select(perspective_ids=perspective_ids, bundle_id=bundle_id)
        return {
            "capability_id": self.capability_id,
            "version": self.version,
            "bundle_id": bundle_id,
            "selected_perspectives": [
                {
                    "id": perspective.perspective_id,
                    "name": perspective.name,
                    "contract_version": perspective.contract_version,
                    "input_schema_ref": perspective.input_schema_ref,
                    "output_schema_ref": perspective.output_schema_ref,
                    "lineage_summary": perspective.lineage_summary,
                    "content": perspective.content,
                }
                for perspective in selected
            ],
        }


class ScholarLoader:
    def __init__(self, scholar_root: Path):
        self.scholar_root = Path(scholar_root)

    @classmethod
    def from_package(cls) -> "ScholarLoader":
        scholar_root = Path(str(files("hldprosim").joinpath("package_data/scholar")))
        return cls(scholar_root=scholar_root)

    def load(self) -> ScholarCatalog:
        pointer_path = self.scholar_root / "pointer.yaml"
        if not pointer_path.exists():
            raise ScholarValidationError(f"Scholar pointer not found: {pointer_path}")

        pointer = yaml.safe_load(pointer_path.read_text())
        if not isinstance(pointer, dict):
            raise ScholarValidationError("Scholar pointer must parse to a mapping")
        missing_pointer_fields = POINTER_REQUIRED_FIELDS - set(pointer)
        if missing_pointer_fields:
            missing = ", ".join(sorted(missing_pointer_fields))
            raise ScholarValidationError(f"Scholar pointer missing required fields: {missing}")

        bundles = pointer.get("bundles") or {}
        if not isinstance(bundles, dict):
            raise ScholarValidationError("Scholar bundles must be a mapping of bundle ids to perspective ids")

        perspectives: dict[str, ScholarPerspective] = {}
        for entry in pointer["perspectives"]:
            self._validate_pointer_entry(entry)
            perspective_path = self.scholar_root / entry["path"]
            if not perspective_path.exists():
                raise ScholarValidationError(
                    f"Scholar perspective file missing for '{entry['id']}': {perspective_path}"
                )
            input_schema_path = self.scholar_root / entry["input_schema_ref"]
            output_schema_path = self.scholar_root / entry["output_schema_ref"]
            if not input_schema_path.exists():
                raise ScholarValidationError(
                    f"Scholar input schema missing for '{entry['id']}': {input_schema_path}"
                )
            if not output_schema_path.exists():
                raise ScholarValidationError(
                    f"Scholar output schema missing for '{entry['id']}': {output_schema_path}"
                )

            frontmatter, body = _parse_markdown_frontmatter(perspective_path.read_text())
            self._validate_frontmatter(entry, frontmatter, perspective_path)

            perspectives[entry["id"]] = ScholarPerspective(
                perspective_id=entry["id"],
                name=entry["name"],
                path=perspective_path,
                contract_version=entry["contract_version"],
                input_schema_ref=entry["input_schema_ref"],
                output_schema_ref=entry["output_schema_ref"],
                lineage_summary=entry["lineage_summary"],
                status=entry["status"],
                content=body.strip(),
                frontmatter=frontmatter,
            )

        for bundle_id, bundle_members in bundles.items():
            if not isinstance(bundle_members, list) or not bundle_members:
                raise ScholarValidationError(f"Scholar bundle '{bundle_id}' must list at least one perspective id")
            for perspective_id in bundle_members:
                if perspective_id not in perspectives:
                    raise ScholarValidationError(
                        f"Scholar bundle '{bundle_id}' references unknown perspective '{perspective_id}'"
                    )

        return ScholarCatalog(
            capability_id=pointer["capability_id"],
            version=pointer["version"],
            pointer_path=pointer_path,
            bundles=bundles,
            perspectives=perspectives,
        )

    def _validate_pointer_entry(self, entry: dict[str, Any]) -> None:
        if not isinstance(entry, dict):
            raise ScholarValidationError("Scholar perspective pointer entries must be mappings")
        missing_entry_fields = POINTER_ENTRY_REQUIRED_FIELDS - set(entry)
        if missing_entry_fields:
            missing = ", ".join(sorted(missing_entry_fields))
            raise ScholarValidationError(f"Scholar pointer entry missing required fields: {missing}")

    def _validate_frontmatter(
        self,
        pointer_entry: dict[str, Any],
        frontmatter: dict[str, Any],
        perspective_path: Path,
    ) -> None:
        missing_frontmatter_fields = PERSPECTIVE_FRONTMATTER_REQUIRED_FIELDS - set(frontmatter)
        if missing_frontmatter_fields:
            missing = ", ".join(sorted(missing_frontmatter_fields))
            raise ScholarValidationError(
                f"Scholar perspective frontmatter missing required fields in {perspective_path.name}: {missing}"
            )
        for field in (
            "id",
            "name",
            "contract_version",
            "input_schema_ref",
            "output_schema_ref",
            "lineage_summary",
        ):
            if str(frontmatter[field]) != str(pointer_entry[field]):
                raise ScholarValidationError(
                    f"Scholar perspective field mismatch for '{pointer_entry['id']}' on '{field}'"
                )


def _parse_markdown_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        raise ScholarValidationError("Scholar perspective markdown must start with YAML frontmatter")
    _, rest = text.split("---\n", 1)
    try:
        frontmatter_text, body = rest.split("\n---\n", 1)
    except ValueError as exc:
        raise ScholarValidationError("Scholar perspective markdown missing frontmatter terminator") from exc
    frontmatter = yaml.safe_load(frontmatter_text)
    if not isinstance(frontmatter, dict):
        raise ScholarValidationError("Scholar perspective frontmatter must parse to a mapping")
    return frontmatter, body
