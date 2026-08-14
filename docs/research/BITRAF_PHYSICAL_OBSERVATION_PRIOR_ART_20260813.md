# BITRAF Physical Observation — bounded prior-art note

Date: 2026-08-13  
Status: `PRIOR_ART_SEED / claim_allowed=false`

Purpose: prevent a broad novelty claim while preserving the narrower BITRAF hypothesis for falsifiable testing.

## Established neighboring work

1. NIST CSRC, **side channel** glossary: indirect effects such as execution time, memory behavior, power-consumption variation and electromagnetic emanations can reveal information while a program executes.
   - https://csrc.nist.gov/glossary/term/side_channel

2. NIST LWC Workshop 2022, **Root-cause Analysis of Power-based Side-channel Leakage in Lightweight Cryptography Candidates**: gate-level power simulation identifies time points with strong data-dependent variation and ranks individual cells by their contribution to power leakage.
   - https://csrc.nist.gov/Presentations/2022/root-cause-analysis-of-power-based-side-channel-le

3. USENIX Security 2015, **Thermal Covert Channels on Multi-core Platforms**: processor-core temperature can form a thermal side/covert channel and can reveal activity on neighboring cores under tested conditions.
   - https://www.usenix.org/conference/usenixsecurity15/technical-sessions/presentation/masti

4. STMicroelectronics, **TIP35C**: epitaxial-base planar bipolar power transistor intended for power linear and switching applications. It is used in this BITRAF branch only as a coarse discrete-device lab analogue.
   - https://www.st.com/en/power-transistors/tip35c.html

## What is therefore NOT claimed as new

- that power variation can correlate with computation;
- that electromagnetic emissions can leak information;
- that temperature can correlate with processor activity;
- that physical side effects can sometimes localize contributing circuitry.

## Candidate BITRAF research delta

The object still requiring comparison and experiment is the integration:

`multichannel physical residue + explicit (x,y,z,t) geometry + topology/path prior + erasure/TOKEN_VAZIO semantics + exact-recovery gate`.

This is a candidate integration/research framing, not a discovery claim.

## Required novelty gate

Before any novelty statement:

1. systematic literature search beyond these seed references;
2. explicit closest-work table;
3. ablation against single-channel power/thermal models;
4. comparison against Cartesian and graph-distance baselines;
5. real held-out measurement;
6. independent replication.

Until then:

```yaml
novelty: TOKEN_VAZIO_PRIOR_ART_SEARCH_INCOMPLETE
claim_allowed: false
```
