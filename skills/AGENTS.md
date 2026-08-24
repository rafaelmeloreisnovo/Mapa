# AGENTS.md — skills/

This directory inherits the repository-root `AGENTS.md`. Nothing here expands authority.

## Skill contract

A `SKILL.md` is a procedural adapter, not evidence and not an authority source.

Before changing a skill:

1. bind current `main`/branch and exact skill path;
2. preserve `DRAFT_FAIL_CLOSED` unless a separate authorized promotion changes lifecycle state;
3. preserve `TOKEN_VAZIO` semantics;
4. do not embed secrets, personal raw data or private Drive locators;
5. update `omega-assurance-skills.v1.json` only when the skill graph itself changes;
6. run `python3 tools/validate_omega_assurance_skills_v1.py` and `python3 -m unittest tests/test_omega_assurance_skills_v1.py`;
7. append a receipt for material lifecycle changes.

## Non-negotiable invariants

```text
skill != authority
skill != evidence
skill_pass != production_pass
capability != authority
prediction != evidence
TOKEN_VAZIO != PASS
```

If a skill conflicts with root `AGENTS.md`, canonical bootstrap, producer authority or a more specific safety/privacy rule, the stricter/higher-authority contract wins and the conflict is recorded as `TOKEN_VAZIO/HOLD`, never silently resolved.
