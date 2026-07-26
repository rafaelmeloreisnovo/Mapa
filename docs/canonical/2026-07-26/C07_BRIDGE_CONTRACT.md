# C07 — Vectras → Termux → QEMU Bridge Contract

**Estado:** `IMPLEMENTED_STATIC_EXECUTION_PENDING`  
**Claim:** `claim_allowed=false`

## Topologia

```text
Vectras consumer
→ bounded request
→ immutable local request record
→ explicit mutable PendingIntent
→ Termux RunCommandService
→ QEMU process
→ Termux result bundle
→ Vectras receiver
→ privacy-minimized receipt
```

## Consumer

Repository: `rafaelmeloreisnovo/Vectras-VM-Android`  
Branch: `c07/vectras-termux-qemu-receipt-2026-07-26`

The consumer now:

- uses a fixed provider package and service;
- requires the dedicated dangerous permission;
- forces `app-shell` runner;
- caps total arguments at 32;
- injects 11 fixed QEMU safety arguments;
- allows at most 21 extra arguments;
- rejects control-character arguments and protected-option overrides;
- hashes a length-prefixed canonical request envelope;
- persists the request before dispatch;
- rejects result intents without a matching local request;
- stores hashes and lengths instead of raw private output.

## Provider

Repository: `rafaelmeloreisnovo/termux-app-rafacodephi`  
Branch: `c07/vectras-provider-contract-2026-07-26`

The provider contract verifies:

- default application id `com.termux.rafacodephi`;
- exported `RunCommandService` protected by `RUN_COMMAND` permission;
- separated path, argv, workdir, runner and PendingIntent extras;
- `app-shell` runner;
- result bundle keys;
- original stdout/stderr lengths;
- separate process exit code and internal service error.

## Result interpretation

```yaml
err_nonzero: TERMUX_INTERNAL_ERROR
err_zero_and_exit_zero: EXECUTED_EXIT_ZERO
err_zero_and_exit_nonzero: EXECUTED_NONZERO
bundle_without_exit: EXECUTION_EXIT_TOKEN_VAZIO
missing_bundle: RESULT_BUNDLE_TOKEN_VAZIO
```

None of these states proves guest boot. Guest boot requires an independent C08 evidence contract.

## Static gates

Consumer:

```sh
python3 tools/verify_vectras_termux_ipc_v3.py --output artifacts/c07/vectras-termux-ipc-v3.json
python3 tools/verify_vectras_termux_ipc_v3_manifests.py
```

Provider:

```sh
python3 scripts/verify_vectras_termux_provider_v3.py --output artifacts/c07/termux-provider-v3.json
```

## Physical gate

C07 closes only when all are observed:

1. Vectras APK hash;
2. Termux APK hash;
3. both package versions installed;
4. RUN_COMMAND permission granted;
5. immutable request file created;
6. dispatch accepted;
7. Termux result bundle received;
8. Vectras receipt written;
9. request and receipt hashes reconciled;
10. raw output not leaked.

## Preserved TOKEN_VAZIO

```yaml
consumer_static_execution: TOKEN_VAZIO
provider_static_execution: TOKEN_VAZIO
android_builds: TOKEN_VAZIO
install_receipts: TOKEN_VAZIO
permission_receipt: TOKEN_VAZIO
real_dispatch: TOKEN_VAZIO
real_result_bundle: TOKEN_VAZIO
qemu_execution: TOKEN_VAZIO
guest_boot: TOKEN_VAZIO
claim_allowed: false
```
