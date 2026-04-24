from hldprosim.scholar import ScholarLoader


def test_scholar_loader_resolves_packaged_pointer_and_perspectives():
    catalog = ScholarLoader.from_package().load()

    assert catalog.capability_id == "scholar"
    assert catalog.version == "0.1.0"
    assert len(catalog.perspectives) == 5
    assert "dow_theorist" in catalog.perspectives
    assert "full_library" in catalog.bundles


def test_scholar_loader_filters_requested_bundle():
    catalog = ScholarLoader.from_package().load()

    context = catalog.build_invocation_context(bundle_id="pattern_scan")
    selected_ids = [entry["id"] for entry in context["selected_perspectives"]]

    assert context["capability_id"] == "scholar"
    assert selected_ids == [
        "classical_chart_pattern_analyst",
        "momentum_indicator_technician",
    ]


def test_scholar_loader_filters_requested_perspectives():
    catalog = ScholarLoader.from_package().load()

    context = catalog.build_invocation_context(
        perspective_ids=["dow_theorist", "momentum_indicator_technician"]
    )
    selected_ids = [entry["id"] for entry in context["selected_perspectives"]]

    assert selected_ids == [
        "dow_theorist",
        "momentum_indicator_technician",
    ]
