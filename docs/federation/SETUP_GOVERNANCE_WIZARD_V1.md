# Setup Governance Wizard Federation V1

State: **PENDING_BUILD_RUNTIME_EVIDENCE**

The federated map points to RafGitTools PR #557. RafGitTools owns the implementation and execution. Mapa stores only routing, state and evidence requirements.

The wizard is intended to provide a post-install, plain-language configuration flow with visible risk, data use, Zero Trust, rollback boundaries and explicit **agree / disagree / decide later** choices.

Material risks must not be hidden in fine print.

The wizard's local custody ledger is app-private and must never contain PATs, tokens, passwords or provider secret values.

A local wizard choice records intent. It does not prove provider permission and does not execute a privileged operation.

Promotion from this map requires exact-head tests, Android build, APK activity presence and launch evidence.
