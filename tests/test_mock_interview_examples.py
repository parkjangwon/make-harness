from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "assets" / "examples"


def test_junior_mock_interview_example_exists_and_shows_safe_default_offers():
    path = EXAMPLES / "mock-interview-junior-developer.md"
    assert path.exists()

    text = path.read_text()

    assert "safe-default mode" in text
    assert "Legacy filename note" in text
    assert "잘 모르겠으면" in text
    assert "기본값" in text
    assert "런타임은" in text
    assert "패키지 매니저는" in text
    assert "부담 없이" in text


def test_senior_mock_interview_example_exists_and_shows_precision_controls():
    path = EXAMPLES / "mock-interview-senior-developer.md"
    assert path.exists()

    text = path.read_text()

    assert "precision mode" in text
    assert "Legacy filename note" in text
    assert "default" in text
    assert "override" in text
    assert "approval" in text
    assert "definition of done" in text
    assert "pnpm" in text or "npm" in text
    assert "This is a one-time setup" not in text
    assert "이건 one-time setup" in text or "이건 일회성 초기 설정" in text


def test_mock_examples_show_same_skill_with_different_depth_not_different_philosophy():
    junior = (EXAMPLES / "mock-interview-junior-developer.md").read_text()
    senior = (EXAMPLES / "mock-interview-senior-developer.md").read_text()

    assert "one-time setup" in junior
    assert "one-time setup" in senior
    assert "user classification" in junior
    assert "user classification" in senior
    assert "repo-first" in junior or "setup-discovery" in junior
    assert "repo-first" in senior or "setup-discovery" in senior
