"""Phase 2 notebook 04a: the command line and the output writing of samples/fea_sweep_gen.py (a local-model draft, reviewed)."""
import json
import subprocess
import sys
from pathlib import Path

SAMPLES = Path(__file__).resolve().parent.parent / "samples"
sys.path.insert(0, str(SAMPLES))
import fea_sweep_gen as g  # noqa: E402


def test_clean_run_creates_expected_structure(tmp_path):
    """Test that a clean run exits 0 and creates the expected files/folders."""
    out = tmp_path / "out"
    result = subprocess.run(
        [sys.executable, str(SAMPLES / "fea_sweep_gen.py"), "--seed", "1", "--out", str(out)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0

    # OUT should contain: paths.tsv, truth.jsonl (empty), and one study-*
    entries = sorted(out.iterdir())
    assert len(entries) == 3

    paths_tsv = out / "paths.tsv"
    truth_jsonl = out / "truth.jsonl"
    study_dirs = [e for e in entries if e.name.startswith("study-")]

    assert paths_tsv.is_file()
    assert truth_jsonl.is_file() and truth_jsonl.stat().st_size == 0
    assert len(study_dirs) == 1


def test_paths_tsv_format_and_content(tmp_path):
    """Test paths.tsv format and that it lists all files correctly."""
    out = tmp_path / "out"
    result = subprocess.run(
        [sys.executable, str(SAMPLES / "fea_sweep_gen.py"), "--seed", "1", "--out", str(out)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0

    study_dir = next(e for e in out.iterdir() if e.name.startswith("study-"))
    lines = (out / "paths.tsv").read_text().strip().split("\n")

    # Every line should be path<TAB>size
    for line in lines:
        assert "\t" in line
        path, size_str = line.rsplit("\t", 1)
        assert int(size_str) == (out / path).stat().st_size

    # Paths should be sorted
    paths = [line.split("\t", 1)[0] for line in lines]
    assert paths == sorted(paths)

    # All files below study-* should be listed
    expected_paths = set()
    for f in (study_dir).rglob("*"):
        if f.is_file():
            rel = str(f.relative_to(out))
            expected_paths.add(rel)

    assert set(paths) == expected_paths
    for p in paths:
        assert p.startswith(study_dir.name + "/")


def test_grid_options_affect_case_count(tmp_path):
    """Test that different grid options produce the expected number of case folders."""
    # Default grid (4x5x3) -> 60 cases
    out1 = tmp_path / "out1"
    result = subprocess.run(
        [sys.executable, str(SAMPLES / "fea_sweep_gen.py"), "--seed", "1", "--out", str(out1)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    study1 = next(e for e in out1.iterdir() if e.name.startswith("study-"))
    cases1 = [e for e in (study1 / "cases").iterdir() if e.is_dir()]
    assert len(cases1) == 60

    # --grid 2x3x1 -> 6 cases
    out2 = tmp_path / "out2"
    result = subprocess.run(
        [sys.executable, str(SAMPLES / "fea_sweep_gen.py"), "--seed", "1", "--grid", "2x3x1", "--out", str(out2)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    study2 = next(e for e in out2.iterdir() if e.name.startswith("study-"))
    cases2 = [e for e in (study2 / "cases").iterdir() if e.is_dir()]
    assert len(cases2) == 6

    # --large -> 600 cases
    out3 = tmp_path / "out3"
    result = subprocess.run(
        [sys.executable, str(SAMPLES / "fea_sweep_gen.py"), "--seed", "1", "--large", "--out", str(out3)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    study3 = next(e for e in out3.iterdir() if e.name.startswith("study-"))
    cases3 = [e for e in (study3 / "cases").iterdir() if e.is_dir()]
    assert len(cases3) == 600


def test_invalid_grid_exits_with_code_2(tmp_path):
    """Test that invalid grids exit with code 2 and write nothing."""
    for grid in ["4x5x4", "4x5", "0x5x3"]:
        out = tmp_path / f"out_{grid.replace('x', '_')}"
        result = subprocess.run(
            [sys.executable, str(SAMPLES / "fea_sweep_gen.py"), "--seed", "1", "--grid", grid, "--out", str(out)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 2
        # OUT should be absent or empty
        if out.exists():
            assert not any(out.iterdir())


def test_large_with_grid_exits_with_code_2(tmp_path):
    """Test that --large with --grid exits with code 2."""
    out = tmp_path / "out"
    result = subprocess.run(
        [sys.executable, str(SAMPLES / "fea_sweep_gen.py"), "--seed", "1", "--large", "--grid", "4x5x3", "--out", str(out)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2


def test_existing_nonempty_out_exits_with_code_2(tmp_path):
    """Test that if OUT exists and holds a file, the run exits with code 2."""
    out = tmp_path / "out"
    out.mkdir()
    (out / "existing.txt").write_text("content")

    result = subprocess.run(
        [sys.executable, str(SAMPLES / "fea_sweep_gen.py"), "--seed", "1", "--out", str(out)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    # The existing file should be unchanged
    assert (out / "existing.txt").read_text() == "content"


def test_spec_file_creates_correct_truth(tmp_path):
    """Test that a spec file creates correct truth.jsonl."""
    import yaml

    out = tmp_path / "out"
    spec = tmp_path / "spec.yaml"
    spec_data = {"mutations": [{"class": "stray-deck"}, {"class": "missing-input-deck"}]}
    spec.write_text(yaml.safe_dump(spec_data))

    result = subprocess.run(
        [sys.executable, str(SAMPLES / "fea_sweep_gen.py"), "--seed", "1", "--out", str(out), "--mutations", str(spec)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0

    truth_lines = (out / "truth.jsonl").read_text().strip().split("\n")
    assert len(truth_lines) == 2

    # Each line should be valid JSON with compact format and sorted keys
    for line in truth_lines:
        obj = json.loads(line)
        assert set(obj.keys()) == {"path", "kind", "status", "class"}
        # Verify compact format (no spaces after separators)
        expected = json.dumps(obj, sort_keys=True, separators=(",", ":"))
        assert line == expected

    # File should end with newline
    assert (out / "truth.jsonl").read_text().endswith("\n")


def test_unknown_class_exits_with_code_2(tmp_path):
    """Test that a spec with unknown class exits with code 2."""
    import yaml

    out = tmp_path / "out"
    spec = tmp_path / "spec.yaml"
    spec_data = {"mutations": [{"class": "nope"}]}
    spec.write_text(yaml.safe_dump(spec_data))

    result = subprocess.run(
        [sys.executable, str(SAMPLES / "fea_sweep_gen.py"), "--seed", "1", "--out", str(out), "--mutations", str(spec)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2


def test_determinism_two_runs(tmp_path):
    """Test that two runs with same arguments give byte-identical outputs."""
    out1 = tmp_path / "out1"
    out2 = tmp_path / "out2"

    for out in [out1, out2]:
        result = subprocess.run(
            [sys.executable, str(SAMPLES / "fea_sweep_gen.py"), "--seed", "1", "--out", str(out)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

    paths1 = (out1 / "paths.tsv").read_bytes()
    paths2 = (out2 / "paths.tsv").read_bytes()
    assert paths1 == paths2

    truth1 = (out1 / "truth.jsonl").read_bytes()
    truth2 = (out2 / "truth.jsonl").read_bytes()
    assert truth1 == truth2


def test_main_direct_call(tmp_path):
    """Test calling g.main() directly."""
    out = tmp_path / "out"
    result = g.main(["--seed", "1", "--out", str(out)])
    assert result == 0
    assert (out / "paths.tsv").exists()
    assert (out / "truth.jsonl").exists()
