# BITRAF Physical Observation — bounded prior-art note

Date: 2026-08-13  
Status: `PRIOR_ART_EXPANDED / claim_allowed=false`

Purpose: prevent a broad novelty claim while preserving the narrower BITRAF hypothesis for falsifiable testing.

## Public neighboring work — chronology

- **2002 — CARDIS / USENIX, Automatic Code Recognition for Smartcards Using a Kohonen Neural Network.** Power and electromagnetic traces were used to recognize instruction signatures and processor actions.
  - https://www.usenix.org/conference/cardis-02/automatic-code-recognition-smartcards-using-kohonen-neural-network

- **2008 — USENIX Security, Lest We Remember: Cold Boot Attacks on Encryption Keys.** DRAM contents can persist after power loss and degraded bit patterns can be handled with error-aware reconstruction.
  - https://www.usenix.org/event/sec08/tech/full_papers/halderman/halderman_html/index.html

- **2011 — NIST, On-Chip Security Using Electromagnetic Analysis.** Electromagnetic monitoring can provide more local information than aggregate power analysis.
  - https://www.nist.gov/publications/chip-security-using-electromagnetic-analysis

- **2013 — ISCA / Carnegie Mellon, An Experimental Study of Data Retention Behavior in Modern DRAM Devices.** Retention behavior depends on data pattern and varies over time, establishing physical retention/leakage as a nontrivial measured phenomenon.
  - https://users.ece.cmu.edu/~omutlu/acaces2013-memory.html

- **2015 — USENIX Security, Thermal Covert Channels on Multi-core Platforms.** Processor-core temperature can reveal activity on neighboring cores under tested conditions.
  - https://www.usenix.org/conference/usenixsecurity15/technical-sessions/presentation/masti

- **2019 — NIST / IEEE VTS, RTL-PSC.** Automated power-leakage assessment can identify internal design blocks that contribute strongly to observed leakage.
  - https://csrc.nist.gov/pubs/conference/2019/04/23/rtlpsc/final

- **2020 — NIST / ACM JETC, Leveraging Side-Channel Information for Disassembly and Security.** Power-supply variation and electromagnetic radiation can support instruction-level hardware monitoring.
  - https://csrc.nist.gov/pubs/journal/2020/02/leveraging-sidechannel-information-for-disassembly/final

- **2020 — MICRO, Bit-Exact ECC Recovery (BEER).** Data-retention behavior can expose hidden ECC structure; the associated BEEP method can recover bit-exact locations of otherwise unobservable raw errors under its experimental model.
  - https://arxiv.org/abs/2009.07985

- **2022 — NIST LWC Workshop, Root-cause Analysis of Power-based Side-channel Leakage.** Gate-level analysis identifies time points of maximum data-dependent variation and ranks individual cells by contribution.
  - https://csrc.nist.gov/Presentations/2022/root-cause-analysis-of-power-based-side-channel-le

- **2022 — USENIX Security, Hiding in Plain Sight?** Physical power/electromagnetic phenomena are used to monitor program execution in embedded systems.
  - https://www.usenix.org/conference/usenixsecurity22/presentation/han

- **2023 — USENIX Security, Hot Pixels.** Internal power, temperature and frequency telemetry on GPUs and Arm SoCs correlates with instructions executed and data processed.
  - https://www.usenix.org/conference/usenixsecurity23/presentation/taneja

## What is therefore NOT claimed as new

- that power variation can correlate with computation;
- that electromagnetic emissions can carry local execution information;
- that temperature can correlate with processor activity;
- that physical side effects can localize contributing circuitry;
- that retention behavior can preserve or expose information after a logical state transition;
- that observable error behavior can constrain hidden ECC/error structure.

## Candidate BITRAF research delta

The object still requiring comparison and experiment is the integration:

`multichannel physical residue + explicit (x,y,z,t) geometry + baseline subtraction + topology/path prior + erasure/TOKEN_VAZIO semantics + separate exact-recovery gate`.

This is a candidate combination/research architecture, not a novelty or patentability conclusion.

## Legal-priority boundary

Internal private records can establish documentary chronology, but they are not automatically public prior art. Public-prior-art status depends on public availability and the applicable legal framework. This repository records provenance and leaves legal conclusions as `TOKEN_VAZIO`.

## Required novelty gate

1. systematic literature and patent search beyond these references;
2. closest-work matrix by claim element;
3. public-availability dates for internal disclosures;
4. ablation against single-channel power/thermal/EM models;
5. comparison against Cartesian and ordinary graph-distance baselines;
6. real held-out measurement and independent replication.

Until then:

```yaml
novelty: TOKEN_VAZIO_PRIOR_ART_SEARCH_INCOMPLETE
legal_priority: TOKEN_VAZIO
claim_allowed: false
```
