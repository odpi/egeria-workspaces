"""PO-61: freshstart's Portal home page (demo-portal.html) was a copy of quickstart's. Its tiles opened
quickstart's ports (Jupyter :8888, Advisor :8880, container Obsidian :8860/:8861), it was titled
"Egeria Quickstart Demo Sandbox · Coco Pharmaceuticals", and it offered a My Egeria tile that 404s
(freshstart does not serve /my-egeria/). These checks read the page as shipped."""
import re
from pathlib import Path

PAGE = (Path(__file__).resolve().parent.parent / "demo-portal.html").read_text(encoding="utf-8")


def _tag_text(tag_id):
    m = re.search(r'id="%s"[^>]*>(.*?)</' % tag_id, PAGE, re.S)
    assert m, tag_id
    return m.group(1)


def test_no_quickstart_ports():
    for port in ("8888", "8880", "8860", "8861"):
        assert not re.search(r"[':]%s\b" % port, PAGE), f"quickstart port {port} still referenced"


def test_jupyter_uses_the_freshstart_port():
    assert PAGE.count(":7888/") == 2          # the Jupyter tile and the notebook deep-link


def test_advisor_falls_back_to_the_freshstart_default():
    assert ":7880/" in PAGE                   # matches EGERIA_ADVISOR_URL's default in demo_config.py


def test_title_and_hero_are_not_quickstart_or_coco():
    title = re.search(r"<title>(.*?)</title>", PAGE, re.S).group(1)
    for text in (title, _tag_text("hdr-title"), _tag_text("hero-title"), _tag_text("hero-sub")):
        assert "Quickstart" not in text and "Coco" not in text, text
    assert "'Egeria Quickstart'" not in PAGE  # the org-name fallback


def test_no_coco_intro_block():
    assert "Coco Pharmaceuticals intro" not in PAGE
    assert "practices/coco-pharmaceuticals\" target=\"_blank\" rel=\"noopener\">Coco Pharmaceuticals" not in PAGE


def test_no_my_egeria_tile():
    assert "/my-egeria/" not in PAGE
