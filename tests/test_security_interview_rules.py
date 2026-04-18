from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_interview_protocol_defines_minimal_security_interview_items_and_storage_mapping():
    protocol = (ROOT / "references" / "interview-protocol.md").read_text()
    skill = (ROOT / "SKILL.md").read_text()

    assert "## Minimal security interview items" in protocol
    assert "sensitive areas" in protocol
    assert "secrets" in protocol
    assert "auth" in protocol
    assert "payment" in protocol
    assert "TLS verification" in protocol
    assert "configuration-based exception" in protocol
    assert "never silently enabled by default" in protocol
    assert "security verification commands" in protocol
    assert "change_guardrails" in protocol
    assert "approval_policy" in protocol
    assert "verification_policy" in protocol
    assert "project_constraints" in protocol
    assert "Do not create a separate heavyweight security framework section" in protocol
    assert "project-local security guardrails" in skill


def test_readme_and_healthy_checklist_explain_security_as_guardrails_not_full_appsec_framework():
    readme = (ROOT / "README.md").read_text()
    checklist = (ROOT / "assets" / "healthy-checklist.md").read_text()

    assert "security-sensitive areas" in readme
    assert "project-local security guardrails" in readme
    assert "not a full AppSec framework" in readme
    assert "configuration-based TLS exception" in readme
    assert "security-sensitive rules" in checklist
