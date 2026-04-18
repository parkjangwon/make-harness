from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_interview_protocol_reference_exists_and_covers_branching_rules():
    protocol = ROOT / "references" / "interview-protocol.md"
    assert protocol.exists()

    text = protocol.read_text()

    assert "## Question order" in text
    assert "## Branching and confidence rules" in text
    assert "README.md before package.json" in text
    assert "package.json scripts override README command guesses" in text
    assert "70%" in text
    assert "confirm" in text


def test_interview_protocol_defines_canonical_normalization_tables():
    protocol = ROOT / "references" / "interview-protocol.md"
    text = protocol.read_text()

    assert "## Canonical normalization" in text
    assert "change_posture" in text
    assert "approval_policy" in text
    assert "verification_policy" in text
    assert "웬만하면 보수적으로" in text
    assert "큰 변경은 먼저 물어봐" in text
    assert "테스트는 있으면 돌리고, 없으면 빌드라도" in text


def test_interview_guide_points_to_protocol_and_resume_rules():
    guide = (ROOT / "references" / "interview-guide.md").read_text()

    assert "[interview protocol](interview-protocol.md)" in guide
    assert "resume" in guide
    assert "temporary inference" in guide
    assert "contradiction" in guide


def test_skill_documents_interview_protocol_resources_and_minimal_question_budget():
    skill = (ROOT / "SKILL.md").read_text()

    assert "interview-protocol.md" in skill
    assert "question budget" in skill
    assert "confirmation questions over open-ended questions" in skill
    assert "one-time setup" in skill
    assert "precision is more important than minimizing question count" in skill


def test_interview_protocol_distinguishes_existing_repos_from_blank_projects():
    protocol = (ROOT / "references" / "interview-protocol.md").read_text()

    assert "## Existing repository mode" in protocol
    assert "## Blank project mode" in protocol
    assert "analyze the codebase first" in protocol
    assert "do not ask for stack or package-manager choices that the repository already answers" in protocol
    assert "ask more upfront because there is no code to inspect" in protocol
    assert "package manager" in protocol
    assert "runtime" in protocol
    assert "one-time setup" in protocol
    assert "precision is more important than minimizing question count" in protocol


def test_interview_guide_mentions_dual_mode_strategy():
    guide = (ROOT / "references" / "interview-guide.md").read_text()

    assert "existing repository" in guide
    assert "blank project" in guide
    assert "repo-first" in guide
    assert "user-facing question templates" in guide
    assert "default" in guide
    assert "junior" in guide
    assert "precision mode" in guide
    assert "safe-default mode" in guide


def test_interview_protocol_includes_existing_repo_and_blank_project_question_templates():
    protocol = (ROOT / "references" / "interview-protocol.md").read_text()

    assert "## Existing repository question templates" in protocol
    assert "## Blank project question templates" in protocol
    assert "패키지 매니저는 npm, pnpm, yarn 중 뭐로 갈까?" in protocol
    assert "이 프로젝트는 웹앱으로 보면 될까?" in protocol
    assert "큰 변경은 먼저 확인받는 쪽이 좋아" in protocol
    assert "테스트/린트까지 통과하면 완료로 볼까?" in protocol
    assert "## Three-level template matrix" in protocol
    assert "high confidence" in protocol
    assert "medium confidence" in protocol
    assert "low confidence" in protocol
    assert "## English companion templates" in protocol
    assert "Would it be okay to treat the default collaboration language as Korean?" in protocol
    assert "Which package manager do you want to use: npm, pnpm, or yarn?" in protocol


def test_interview_protocol_covers_three_levels_for_core_fields():
    protocol = (ROOT / "references" / "interview-protocol.md").read_text()

    assert "### communication_language" in protocol
    assert "### project_type" in protocol
    assert "### definition_of_done" in protocol
    assert "### approval_policy" in protocol
    assert "### project_commands" in protocol
    assert "KO high:" in protocol
    assert "KO medium:" in protocol
    assert "KO low:" in protocol
    assert "EN high:" in protocol
    assert "EN medium:" in protocol
    assert "EN low:" in protocol
    assert "If you're not sure, I can suggest a safe default" in protocol
    assert "잘 모르겠으면 내가 무난한 기본값을 먼저 제안할게" in protocol
    assert "two-step questioning" in protocol
    assert "start with an easy default-offer question" in protocol
    assert "## Adaptive response modes" in protocol
    assert "precision mode" in protocol
    assert "clarify mode" in protocol
    assert "safe-default mode" in protocol
    assert "do not classify the user as junior or senior" in protocol
    assert "adapt per answer, not per person label" in protocol


def test_fixture_set_covers_interview_resume_conflicting_signals_and_blank_bootstrap_cases():
    resume_fixture = ROOT / "assets" / "fixtures" / "resume-interview-after-partial-confirmation" / "fixture.json"
    conflicting_signals = ROOT / "assets" / "fixtures" / "bootstrap-conflicting-signals" / "fixture.json"
    blank_bootstrap = ROOT / "assets" / "fixtures" / "bootstrap-empty-project-stack-discovery" / "fixture.json"

    assert resume_fixture.exists()
    assert conflicting_signals.exists()
    assert blank_bootstrap.exists()

    assert '"bootstrap_status": "interview_in_progress"' in resume_fixture.read_text()
    assert '"repo_language_signal": "mixed"' in conflicting_signals.read_text()
    assert '"package_manager"' in blank_bootstrap.read_text()
