import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

REQUIRED_FILES = [
    "R223Q_generation_regression_plan.md",
    "R223Q_sample_generation_inputs.json",
    "R223Q_generated_teacher_default_drafts/M_stationery_teacher_default_draft.md",
    "R223Q_generated_teacher_default_drafts/N_paper_print_teacher_default_draft.md",
    "R223Q_generated_teacher_default_drafts/O_color_collision_teacher_default_draft.md",
    "R223Q_generated_review_ledgers/M_stationery_review_ledger.json",
    "R223Q_generated_review_ledgers/N_paper_print_review_ledger.json",
    "R223Q_generated_review_ledgers/O_color_collision_review_ledger.json",
    "R223Q_teacher_default_view_quality_check.md",
    "R223Q_review_ledger_completeness_check.md",
    "R223Q_unit_intensity_effect_check.md",
    "R223Q_component_trigger_safety_check.md",
    "R223Q_regression_decision_report.md",
    "PACKAGE_MANIFEST.json",
    "README_FOR_GPT_REVIEW.md",
]

SAMPLES = ["M_stationery", "N_paper_print", "O_color_collision"]
FORBIDDEN_TEACHER_TERMS = [
    "practice_pattern_type",
    "demonstration_type",
    "micro_practice_type",
    "appreciation_scaffold_type",
    "component_trigger",
    "component_trigger_status",
    "screen_trigger",
    "learning_sheet_fields",
    "primary_pattern",
    "secondary_patterns",
]
LEDGER_REQUIRED = [
    "unit_phase_role",
    "practice_intensity",
    "teacher_support_density",
    "events",
]
EVENT_REQUIRED = [
    "event_id",
    "primary_pattern",
    "component_trigger",
    "screen_trigger",
    "learning_sheet_fields",
    "evidence_outputs",
]
BOUNDARY_FALSE = [
    "schema_v0_2_published",
    "formal_ui",
    "r97b_modified",
    "frontend_backend_modified",
    "formal_runtime_connected",
    "provider_model_connected",
    "prompt_modified",
    "database_written",
    "lesson_body_written",
    "existing_teacher_drafts_modified",
    "r222d_component_library_modified",
    "formal_apply",
]
STATUS_VALUES = ["already_registered", "candidate_from_R222D_pool", "new_surface_candidate", "unregistered_do_not_execute"]


def add(checks, name, passed, detail=None):
    item = {"check": name, "passed": bool(passed)}
    if detail is not None:
        item["detail"] = detail
    checks.append(item)


def read(path):
    return path.read_text(encoding="utf-8")


def load_json(path):
    return json.loads(read(path))


def main():
    checks = []

    for name in REQUIRED_FILES:
        add(checks, f"required_file:{name}", (ROOT / name).exists())

    manifest = load_json(ROOT / "PACKAGE_MANIFEST.json")
    inputs = load_json(ROOT / "R223Q_sample_generation_inputs.json")

    add(checks, "manifest_stage", manifest.get("stage_id") == "1013R_R223Q_TRUE_GENERATION_REGRESSION_GATE")
    add(checks, "decision", manifest.get("decision") == "PASS_CONTINUE_TO_R223R_V0_2_CANDIDATE_PILOT_ROUTE_PLANNING")
    for flag in BOUNDARY_FALSE:
        add(checks, f"boundary_false:{flag}", manifest.get(flag) is False)

    input_samples = {item["sample_id"]: item for item in inputs.get("samples", [])}
    for sample_id in SAMPLES:
        add(checks, f"input_sample:{sample_id}", sample_id in input_samples)
        draft = ROOT / "R223Q_generated_teacher_default_drafts" / f"{sample_id}_teacher_default_draft.md"
        ledger = ROOT / "R223Q_generated_review_ledgers" / f"{sample_id}_review_ledger.json"
        add(checks, f"draft_exists:{sample_id}", draft.exists())
        add(checks, f"ledger_exists:{sample_id}", ledger.exists())
        if draft.exists():
            text = read(draft)
            for term in FORBIDDEN_TEACHER_TERMS:
                add(checks, f"teacher_no_forbidden:{sample_id}:{term}", term not in text)
            add(checks, f"teacher_has_goal:{sample_id}", "教学目标" in text)
            add(checks, f"teacher_has_process:{sample_id}", "教学过程" in text)
            add(checks, f"teacher_has_evidence:{sample_id}", "评价证据" in text)
        if ledger.exists():
            data = load_json(ledger)
            for key in LEDGER_REQUIRED:
                add(checks, f"ledger_key:{sample_id}:{key}", key in data)
            events = data.get("events", [])
            add(checks, f"ledger_event_count:{sample_id}", len(events) >= 5)
            for event in events:
                eid = event.get("event_id", "unknown")
                for key in EVENT_REQUIRED:
                    add(checks, f"event_key:{sample_id}:{eid}:{key}", key in event)
                for trigger in event.get("component_trigger", []):
                    add(checks, f"component_status:{sample_id}:{eid}:{trigger.get('component_id')}", trigger.get("status") in STATUS_VALUES)

    ledgers = [load_json(ROOT / "R223Q_generated_review_ledgers" / f"{sample_id}_review_ledger.json") for sample_id in SAMPLES]
    profiles = {(item.get("unit_phase_role"), item.get("practice_intensity"), item.get("teacher_support_density")) for item in ledgers}
    add(checks, "distinct_density_profiles", len(profiles) >= 2, sorted(map(str, profiles)))

    report = read(ROOT / "R223Q_regression_decision_report.md")
    for phrase in ["PASS_LOCAL_GENERATION_REGRESSION_GATE", "R223M_STANDARD_V0_2 = NOT_PUBLISHED", "NEXT_ALLOWED"]:
        add(checks, f"report_phrase:{phrase}", phrase in report)

    for name in [
        "R223Q_teacher_default_view_quality_check.md",
        "R223Q_review_ledger_completeness_check.md",
        "R223Q_unit_intensity_effect_check.md",
        "R223Q_component_trigger_safety_check.md",
    ]:
        text = read(ROOT / name)
        add(checks, f"check_doc_pass:{name}", "PASS" in text)

    failures = [check for check in checks if not check["passed"]]
    result = {
        "passed": not failures,
        "check_count": len(checks),
        "failed": len(failures),
        "failures": failures,
        "decision": "PASS_CONTINUE_TO_R223R_V0_2_CANDIDATE_PILOT_ROUTE_PLANNING" if not failures else "HOLD_FOR_GENERATION_QUALITY_REWORK",
        "checks": checks,
    }
    (ROOT / "validate_1013R_R223Q_true_generation_regression_gate_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: result[k] for k in ["passed", "check_count", "failed", "decision"]}, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
