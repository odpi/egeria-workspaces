"""egeria-overview.html: Semantic Grounding says what it measures, and is a % only when it is a share."""
from pathlib import Path

HTML = (Path(__file__).resolve().parent.parent / "egeria-overview.html").read_text()


def test_grounding_tile_is_never_a_percent_unless_pyegeria_reports_an_asset_share():
    assert "const groundingIsShare = s => s.groundingMeasure === 'assetShare';" in HTML
    assert "(groundingIsShare(s) ? s.groundingValue + '%' : num(s.groundingValue))" in HTML
    assert "'term links per 100 Assets'" in HTML
    # nothing renders the old links-based groundingPct with a % sign
    assert "groundingPct + '%'" not in HTML and "d.groundingPct + '%'" not in HTML


def test_grounding_static_tile_and_sources_use_the_new_fields():
    assert 'id="ai-grounding-sub">term links per 100 Assets<' in HTML
    assert "setTxt('ai-grounding-sub', groundingSub(d))" in HTML
    assert "'ai-context': 'groundingLinks'" in HTML                    # stale-source check: a field that is always set
    assert "grounding:s=>s.groundingValue" in HTML


def test_ownership_tile_reads_owned_assets():
    assert "num(LIVE.ownershipCount) + ' owned assets'" in HTML


def test_ownership_tile_names_its_population():
    # "416 owned assets · whole catalog": a screenshotted tile says whose Assets it counts (Architect P3)
    assert "ownership:'scopeOwnership'" in HTML
    assert "store.scopeOwnership = d.ownershipScope || null;" in HTML
