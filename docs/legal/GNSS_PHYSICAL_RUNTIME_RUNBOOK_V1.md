# RAFAELIA — GNSS Physical Runtime Runbook V1

**State:** `READY_FOR_AUTHORIZED_PHYSICAL_EXECUTION`  
**Claim boundary:** `claim_allowed=false`  
**F_next:** `FN-GNSS-002`  
**Purpose:** produce exactly one minimized, byte-hashed, auditable Android GNSS runtime receipt without promoting network/model/legal claims.

## Mother invariant

```text
build_success != installed_build != physical_runtime != evidence != claim
field_available != field_retained
local_receipt != network_transfer
network_transfer != model_context_access
receipt_hash_seal != reproducibility
claim_precision <= evidence_precision
TOKEN_VAZIO != false
```

Urgency never authorizes skipping a gate.

## Canonical producer build

Producer repository:

```text
rafaelmeloreisnovo/termux-api_rafcodephi
branch: master
head: 50cc6e8f618c70145fc2365467935d542fe8ef17
```

Verified CI evidence:

```text
workflow: Advanced Hardcoded CI Build
run_id: 33026629120
conclusion: SUCCESS
artifact: advanced-hardcoded-apks
artifact_id: 9628699094
artifact_size_bytes: 26668157
artifact_digest: sha256:e5db2835bfa31f14bfa17aacb90c6c7723bd05ac4089715ad84148b4352447ac
```

The workflow passed debug/release build, ARM32/ARM64 validation, internal validation signing, destruction of the temporary validation private key, checksums, and artifact upload.

**This proves buildability only. It does not prove installation or GNSS runtime.**

## Gate 0 — protect the installed app/signing lineage

Android package updates require compatible signing lineage. The CI release APK is signed with an **internal validation key that is destroyed after the CI run**. Therefore it must not be treated as a durable production/update key.

Before replacing an already installed Termux:API variant:

1. identify the installed package and signer;
2. inspect the candidate APK signer;
3. if the signer lineage is incompatible, **do not force an update**;
4. use a controlled test installation/profile/device or rebuild the same source with an authorized compatible signing key.

Example inspection when Android build-tools are available:

```bash
apksigner verify --verbose --print-certs candidate.apk
```

If the installed signer cannot be established, record:

```text
TOKEN_VAZIO_INSTALLED_SIGNER
```

and stop the update path rather than uninstalling data blindly.

## Gate 1 — choose the ABI intentionally

Use only the APK matching the target runtime ABI.

Expected build families include:

```text
armeabi-v7a   -> ARM32
arm64-v8a     -> ARM64
```

Do not infer ABI from marketing model name. On the target Android/Termux environment, record the observed ABI, for example:

```bash
getprop ro.product.cpu.abi
uname -m
```

A mismatch is a `HOLD`, not an installation experiment.

## Gate 2 — permissions and device state

Required for this collector:

```text
ACCESS_FINE_LOCATION = GRANTED
Location/GPS service = enabled/observable
request = gnss-receipt
provider = gps
authorized_test = true
```

Raw GNSS measurement support is **not guaranteed** by Android version alone. If callbacks or fields are absent, preserve `TOKEN_VAZIO`/`NOT_OBSERVED`; do not infer hardware defect.

The collector deliberately excludes unrelated personal-data surfaces:

```text
contacts = excluded
SMS = excluded
call log = excluded
microphone = excluded
precise coordinate values = not retained
NMEA sentences = not retained
SVID/PRN values = not retained
raw measurement values = not retained
```

## Gate 3 — one bounded local capture

From the checked-out producer repository on the authorized device:

```bash
bash scripts/gnss-runtime-receipt.sh 8000 Brazil true
```

Equivalent low-level request:

```bash
termux-api Location \
  --es provider gps \
  --es request gnss-receipt \
  --ez authorized_test true \
  --ei duration_ms 8000 \
  --ez raw_measurements true \
  --es jurisdiction Brazil
```

Default output directory:

```text
$HOME/PEDRA_ANGULAR/sensors/raw/
```

Expected pair:

```text
gnss_runtime_receipt_<timestamp>.json
gnss_runtime_receipt_<timestamp>.json.sha256
```

No network upload is part of the helper.

## Gate 4 — verify exact bytes before interpretation

Immediately verify the sidecar:

```bash
cd "$HOME/PEDRA_ANGULAR/sensors/raw"
sha256sum -c gnss_runtime_receipt_<timestamp>.json.sha256
```

Required result:

```text
OK
```

A digest failure means `HOLD`; do not repair the JSON by hand.

## Gate 5 — validate the GNSS receipt contract

With the `Mapa` repository available locally:

```bash
python3 scripts/validate_gnss_runtime_receipt.py \
  "$HOME/PEDRA_ANGULAR/sensors/raw/gnss_runtime_receipt_<timestamp>.json"
```

Only a validator PASS may advance the receipt into the provenance stage.

A PASS still means:

```text
valid_receipt != downstream_boundary_proof
valid_receipt != legal_compliance
valid_receipt != reproducibility
```

## Gate 6 — seal provenance append-only

Pin the exact producer commit used for the installed/captured build. For the CI-evidenced source in this runbook:

```text
50cc6e8f618c70145fc2365467935d542fe8ef17
```

Create the specialized evidence-closure record:

```bash
python3 scripts/seal_gnss_runtime_evidence.py \
  "$HOME/PEDRA_ANGULAR/sensors/raw/gnss_runtime_receipt_<timestamp>.json" \
  --producer-repo rafaelmeloreisnovo/termux-api_rafcodephi \
  --producer-commit 50cc6e8f618c70145fc2365467935d542fe8ef17 \
  --output "$HOME/PEDRA_ANGULAR/sensors/raw/gnss_runtime_evidence_<timestamp>.jsonl"
```

Then validate the generic federation closure contract too:

```bash
python3 tools/validate_evidence_closure.py \
  "$HOME/PEDRA_ANGULAR/sensors/raw/gnss_runtime_evidence_<timestamp>.jsonl"
```

The seal intentionally emits:

```text
status = EVIDENCED
claim_allowed = false
REPRODUCIBILITY = TOKEN_VAZIO
```

because one physical observation is not a reproducibility proof.

## Gate 7 — interpret only the observed field states

Allowed from one validated receipt:

```text
OBSERVED        -> field/callback presence demonstrated in this bounded run
NOT_OBSERVED    -> relevant callback/source existed but this field state was not observed
REDACTED        -> field existed but value was intentionally not retained
TOKEN_VAZIO     -> evidence insufficient to decide
```

Forbidden promotions include:

```text
one-device observation -> all Android devices
raw measurement callback -> derived pseudorange correctness
local callback -> network transmission
network transmission -> assistant/model context
build PASS -> runtime PASS
technical PASS -> legal compliance
```

## Gate 8 — downstream boundaries remain independent

After the physical receipt is sealed, the next probes are independent:

```text
ANDROID_TO_APP
APP_TO_SERVICE
SERVICE_TO_TOOL
TOOL_TO_ASSISTANT_CONTEXT
ASSISTANT_CONTEXT_TO_MODEL
APP_TO_THIRD_PARTY
```

A PASS on one edge does not propagate to another edge.

Without runtime packet capture, `APP_TO_THIRD_PARTY` remains `TOKEN_VAZIO`.
Without service/tool/model-context instrumentation, the corresponding downstream edges remain `TOKEN_VAZIO`.

## Gate 9 — second run before reproducibility promotion

Repeat only after the first receipt has been preserved and sealed. A second run must retain its own timestamp, bytes, digest and provenance; never overwrite the first receipt.

Numeric or field equality alone does not establish same-run identity or reproducibility.

## Failure semantics

```text
permission denied                    -> HOLD / fix permission, rerun as new receipt
GPS callback absent                  -> TOKEN_VAZIO or NOT_OBSERVED according to source state
raw callback registration unavailable -> TOKEN_VAZIO
no raw measurement event             -> TOKEN_VAZIO/NOT_OBSERVED; no hardware-failure inference
receipt schema FAIL                  -> HOLD
SHA-256 FAIL                         -> HOLD / preserve original bytes
signer mismatch                      -> HOLD / do not force update
ABI mismatch                         -> HOLD
network boundary not instrumented    -> TOKEN_VAZIO
model-context boundary not observed  -> TOKEN_VAZIO
```

## Current closure state

```text
FN-GNSS-001                    = CLOSED_PASS
FN-GNSS-002 / BUILD            = CLOSED_PASS
FN-GNSS-002 / PHYSICAL_RUNTIME = WAITING_EXTERNAL_RUNTIME
FN-GNSS-003 / TOOLING          = READY_AND_CI_VALIDATED
FN-GNSS-003 / RUNTIME_INPUT    = TOKEN_VAZIO
FN-GNSS-004..007               = TOKEN_VAZIO
FN-CONT-008                    = READY
FN-PRIVATE-009                 = BLOCKED
```

## R3

```text
F_ok   = corrected producer + exact green build + artifact digest + receipt validator + provenance sealer + fail-closed runbook
F_gap  = first physical Android receipt + byte seal + downstream boundary evidence + second-run reproducibility
F_next = execute exactly one authorized/minimized physical receipt, verify SHA-256, validate, seal, then advance only the edges actually evidenced
```
