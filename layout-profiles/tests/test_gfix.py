"""G-FIX: config_sha256 is semantic for the grammar lists. A grammar item enters configuration.canonical() as a dict of its semantic fields only (no repr(),
no evidence, tuned_on or origin); required, allowed_only and content_checks enter only when the profile has them, so a profile without them keeps its hash.
Synthetic edits of the shipped bids-dataset profile only."""
import copy
import dataclasses
from pathlib import Path

import pytest
import yaml

from recognizer import configuration as cfg
from recognizer import grammar as gm
from recognizer.layout_profile import load_profile, parse_profile

PROFILES = Path(__file__).resolve().parent.parent / "profiles"
BIDS = yaml.safe_load((PROFILES / "bids-dataset.yaml").read_text(encoding="utf-8"))
G1_LISTS = ("path_grammar", "name_grammar", "required", "allowed_only", "content_checks")


def sha(doc) -> str:
    return cfg.config_sha256(parse_profile(doc, "x", PROFILES, _shipped=True))


BASE = sha(copy.deepcopy(BIDS))


def test_the_shipped_profile_hashes_as_loaded():
    assert BASE == cfg.config_sha256(load_profile("bids-dataset", PROFILES))


@pytest.mark.parametrize("name", sorted(cfg.GRAMMAR_KEEP))
def test_every_field_of_a_grammar_class_is_kept_or_dropped(name):
    fields = {f.name for f in dataclasses.fields(getattr(gm, name))}
    keep, drop = set(cfg.GRAMMAR_KEEP[name]), set(cfg.GRAMMAR_DROP[name])
    assert not keep & drop and keep | drop == fields, f"{name}: a field is neither kept nor dropped: {sorted(fields - keep - drop)}"
    assert {"evidence", "tuned_on", "origin"} <= drop


def test_the_canonical_form_has_no_repr_and_no_documentation():
    canon = cfg.canonical(load_profile("bids-dataset", PROFILES))
    for k in G1_LISTS:
        assert canon[k] and all(isinstance(x, dict) and not {"evidence", "tuned_on", "origin"} & set(x) for x in canon[k]), k
    blob = repr(canon)
    assert "PathPattern(" not in blob and "re.compile(" not in blob


@pytest.mark.parametrize("key", G1_LISTS)
def test_an_evidence_or_tuned_on_edit_leaves_the_hash(key):
    doc = copy.deepcopy(BIDS)
    for item in doc[key]:
        item["evidence"] = "other words, " + item["evidence"]
        item["tuned_on"] = ["somewhere else"]
    assert sha(doc) == BASE


def test_an_origin_change_leaves_the_hash():
    p = load_profile("bids-dataset", PROFILES)
    moved = dataclasses.replace(p, **{k: tuple(dataclasses.replace(x, origin="elsewhere") for x in getattr(p, k)) for k in G1_LISTS})
    assert cfg.config_sha256(moved) == cfg.config_sha256(p)


def _first(doc, key, pred=lambda x: True):
    return next(x for x in doc[key] if pred(x))


SEMANTIC_EDITS = {
    "a path pattern": lambda d: _first(d, "path_grammar").__setitem__("pattern", _first(d, "path_grammar")["pattern"].replace("sub-", "subj-")),
    "a path token regex": lambda d: _first(d, "path_grammar", lambda x: "regex" in str(x["tokens"]))["tokens"].update(
        {k: {"regex": "[0-9]+"} for k, v in _first(d, "path_grammar", lambda x: "regex" in str(x["tokens"]))["tokens"].items() if "regex" in v}),
    "a path pattern's confidence": lambda d: _first(d, "path_grammar").__setitem__("confidence", "low" if _first(d, "path_grammar")["confidence"] != "low" else "high"),
    "a name grammar label": lambda d: _first(d, "name_grammar").__setitem__("label", "[a-z]+"),
    "a required entry": lambda d: _first(d, "required").__setitem__("id", _first(d, "required")["id"] + "-x"),
    "an allowed_only entry": lambda d: _first(d, "allowed_only").__setitem__("files", list(_first(d, "allowed_only").get("files", [])) + ["EXTRA.txt"]),
    "a content check": lambda d: _first(d, "content_checks", lambda x: "check" in x)["check"].update(
        {"regex": "^9.*$"} if "regex" in _first(d, "content_checks", lambda x: "check" in x)["check"] else {"non_empty": False}),
    "a grammar item order": lambda d: d["path_grammar"].reverse(),
}


@pytest.mark.parametrize("what", sorted(SEMANTIC_EDITS))
def test_a_semantic_change_moves_the_hash(what):
    doc = copy.deepcopy(BIDS)
    SEMANTIC_EDITS[what](doc)
    assert doc != BIDS, f"{what}: the edit changed nothing"
    try:
        moved = sha(doc)
    except Exception as exc:                                     # an edit the loader refuses is not a test of the hash
        pytest.fail(f"{what}: the edited profile does not load: {exc}")
    assert moved != BASE, what


@pytest.mark.parametrize("profile", ["code-repo-conventions", "code-repo", "docs-site", "workspace-repo", "generic-relevance"])
def test_a_profile_without_the_optional_grammar_lists_leaves_them_out(profile):
    canon = cfg.canonical(load_profile(profile, PROFILES))
    assert not set(cfg.GRAMMAR_OPTIONAL) & set(canon)
    assert canon["path_grammar"] == [] and canon["name_grammar"] == []
