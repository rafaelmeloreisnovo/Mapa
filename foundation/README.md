# RAFAELIA Foundation V1

This package turns a downloaded repository into a local, auditable Termux
checkout without assuming that all repositories share one compiler, one
runtime, or one kind of evidence.

The foundation is deliberately small:

    Mapa/foundation
      -> target/.rafaelia/foundation.yaml
      -> target/termux/autoexec-rafaelia.sh
      -> target/COMPILA/<run-id>/receipt.json
      -> target/COMPILA/<run-id>/gate.computational.v1-<UTC>.json

The manifest is JSON-form YAML 1.2. It is therefore readable by YAML tools but
is parsed with the Python standard library; no PyYAML, API, network service,
cloud runner, or shell string evaluation is required.

## Operational topology

| Layer | Location | Responsibility |
|---|---|---|
| Canonical package | `Mapa/foundation/` | Generator, contract schema, template and tests |
| Per-repository declaration | `.rafaelia/foundation.yaml` | Explicit profile, inputs and commands |
| Mobile entry point | `termux/autoexec-rafaelia.sh` | Executes plan, verify or one named profile |
| Local evidence | `COMPILA/<run-id>/` | Environment, input hashes, command events, logs and receipt |
| Cross-repository state | `Mapa` | Records which repository and receipt may be reviewed |

The runner permits only argument-vector commands. It calls subprocesses with
shell disabled and never applies an implicit build profile from detected files.
That prevents a README, a language extension, or an analogy between projects
from becoming an unreviewed execution decision.

## One checkout, one explicit profile

From an existing local clone of Mapa and a second cloned repository:

    cd /data/data/com.termux/files/home/Mapa
    python3 foundation/scripts/rafaelia_foundation.py init \
      --repo-root ../RafPolimata \
      --project-id rafpolimata-local \
      --profile freestanding-object \
      --source src/entry.c

Then enter the target repository:

    cd ../RafPolimata
    bash termux/autoexec-rafaelia.sh plan --profile freestanding-object
    bash termux/autoexec-rafaelia.sh verify --profile freestanding-object
    bash termux/autoexec-rafaelia.sh run freestanding-object

The source path is always repository-relative. Initialization refuses to
overwrite an existing Foundation file. A target may be reconfigured only by a
deliberate edit to its manifest, followed by a new receipt.

## Built-in profiles

| Profile | What it does | What it does not claim |
|---|---|---|
| `documentation` | Checks declared documentation inputs and creates a structural receipt | Build, execution or behavior |
| `python` | Compiles one chosen Python file into the run directory | Application behavior or test coverage |
| `freestanding-object` | Uses clang to create a C or assembly object with freestanding compile flags | Linked ELF, Android installation or device behavior |
| `make` | Runs the explicit default Make target | Correctness beyond its own command outcome |
| `cmake` | Configures and builds into the selected `COMPILA` run directory | Android/Gradle compatibility or deployment |

Android APK builds require the Android SDK and a project-specific contract.
They are not inferred or silently attempted on Termux. A project that has a
validated host may add an explicit argv profile to its manifest; the receipt
still remains local evidence until linked to a repository state and reviewed.

## Receipt contract

Each plan, verification or execution creates a new directory:

    COMPILA/<UTC-run-id>/
      environment.json
      input_manifest.json
      plan.json
      commands.jsonl
      stdout.log
      stderr.log
      receipt.json
      receipt.sha256

Every regular artifact produced below the run directory is hashed, including a
target-provided `test-summary.json`; input files and the copied runner are
hashed separately. The runner also records the local Git `HEAD`, whether the
worktree was clean, the observed runtime, and resolved executable identities.
It does not scan the complete checkout, copy credentials, send telemetry,
modify Git state, or replace a previous receipt. `COMPILA/.gitignore` prevents
accidental publication of raw local logs; an accepted receipt can be copied
into a repository audit path in a separate, reviewed change.

## States

The Foundation preserves these distinctions:

    source != implementation != execution != evidence != claim

`PASS_PREFLIGHT_ONLY` means the declared paths and tools are available.
`PASS_LOCAL_EXECUTION` means the selected argv list exited successfully in the
recorded local environment. Neither state changes `claim_allowed`, which stays
false in every manifest and receipt. Missing source, profile or tool is
recorded as `TOKEN_VAZIO`, with a concrete next action.

## Computational review gate

`PASS_LOCAL_EXECUTION` is not yet a computational review decision. A target
profile that runs tests must write a `rafaelia.test-summary/v1` document inside
its own `{{OUT}}` directory, with its discovered/executed/passed/failed/skipped
counts, each test result, and explicit exercised falsifiers. Then run:

    python3 foundation/scripts/gate_computational_v1.py \
      --repo-root /caminho/do/checkout \
      --receipt COMPILA/<run-id>/receipt.json \
      --test-summary COMPILA/<run-id>/test-summary.json \
      --expected-profile <profile-explícito>

The gate hashes and checks the receipt, input bytes, current clean Git `HEAD`,
environment, command events, test inventory and falsifiers. Its only positive
result is `READY_FOR_DOMAIN_SPECIFIC_REVIEW`; it never changes
`claim_allowed=false`. See
[`GATE_COMPUTATIONAL_V1.md`](../docs/canonical/2026-07-31/GATE_COMPUTATIONAL_V1.md).

## Extend a profile safely

Add a profile only as a list of literal executable arguments. For example, a
project may declare a relative script such as `./gradlew` or a compiler command
with a named source and output. Do not use a shell wrapper, `sh -c`, `eval`,
network bootstrap, automatic package installation, or an absolute path.

The schema documents the contract, and the runner performs the fail-closed
checks in the Python standard library.
