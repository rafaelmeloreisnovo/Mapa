# Runbook — RAFAELIA Vertical Slice V1

## Reference/desktop

```sh
python3 scripts/run_vertical_slice_v1.py \
  --source-root /path/to/sources \
  --repository-root . \
  --runtime-class REFERENCE_RUNTIME
python3 gates/vertical_slice_v1_gate.py
```

## Android Termux

```sh
chmod +x termux/run_rafaelia_vertical_slice_v1.sh
./termux/run_rafaelia_vertical_slice_v1.sh /sdcard/Download
```

Do not overwrite the reference receipt. The Termux runner writes `RECEIPT-VSLICE-001.termux.json` as a separate append-only observation. Record the exact commit and review outcome before any maturity promotion.
