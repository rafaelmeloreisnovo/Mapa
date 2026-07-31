# RafPolimata compiler adapter V1

This is an explicit adapter for `rafaelmeloreisnovo/RafPolimata`; it does not
detect repositories by name, source extension, or environment. It binds the
existing tracked local compiler test:

```text
scripts/validate_runtime_truth_local.sh
```

to Foundation receipts and `gate.computational.v1` test accounting.

## Provision one checkout

From the checkout that contains `Mapa/foundation`:

```sh
python3 foundation/scripts/rafaelia_foundation.py init \
  --repo-root ../RafPolimata \
  --project-id rafpolimata-local \
  --adapter rafpolimata-compiler-gate
```

The initializer copies only these declared Foundation files:

```text
.rafaelia/foundation.yaml
.rafaelia/tools/rafaelia_foundation.py
.rafaelia/tools/gate_computational_v1.py
.rafaelia/README.md
termux/autoexec-rafaelia.sh
scripts/rafpolimata_foundation_compiler_gate.py
COMPILA/.gitignore
```

It never overwrites an existing Foundation path, installs packages, fetches
network data, edits Git metadata, commits, or executes the compiler.

The provisioning files must be part of the checked-out commit before a gate can
bind execution to a clean `HEAD`. Until then, `TOKEN_VAZIO_GIT_WORKTREE_NOT_CLEAN`
is the correct result.

## Local sequence

Inside the provisioned, clean RafPolimata checkout:

```sh
bash termux/autoexec-rafaelia.sh plan --profile compiler-local-gate
bash termux/autoexec-rafaelia.sh verify --profile compiler-local-gate
bash termux/autoexec-rafaelia.sh run compiler-local-gate
```

The adapter calls its tracked script directly through `subprocess` argv, not
through `sh -c`. It writes `test-summary.json` inside the run directory. The
summary enumerates the nine known blocks, preserves failure/not-executed state
on an early exit, and marks the existing negative tests as falsifiers only when
the full script reports success.

Then gate the exact run:

```sh
bash termux/autoexec-rafaelia.sh gate \
  --receipt COMPILA/<run-id>/receipt.json \
  --test-summary COMPILA/<run-id>/test-summary.json \
  --expected-profile compiler-local-gate
```

The only positive result is `READY_FOR_DOMAIN_SPECIFIC_REVIEW`. It does not
promote compiler correctness, ELF/DEX/APK behavior, Android installation,
scientific claims, or any legal/security claim.
