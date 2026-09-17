# OECG V1 scope / population rule

Every metric, PASS, failure, contradiction and claim must name its scope/population/window where relevant.

Examples:

- `fixture PASS` is not `repository PASS`;
- `repository CI PASS` is not `device/runtime PASS`;
- `one dataset result` is not `population-wide result`;
- `historical state` is not `current state`;
- `current branch` is not `all repositories`.

Cross-scope promotion requires an explicit evidence bridge.
