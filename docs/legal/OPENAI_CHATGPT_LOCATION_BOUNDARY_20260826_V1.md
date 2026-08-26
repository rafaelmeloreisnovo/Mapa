# OpenAI / ChatGPT — Location & GNSS Product Boundary — 2026-08-26 V1

Status: **POLICY/DOCUMENTATION VERIFIED · RAW GNSS RUNTIME TOKEN_VAZIO**  
Parent canon: `docs/legal/GLOBAL_DATA_PRIVACY_GNSS_AI_GOVERNANCE_V1.md`  
`claim_allowed=false`

## 1. Current public-product evidence

Observed against current OpenAI public materials on 2026-08-26:

1. OpenAI's Brazil privacy policy, updated 2026-07-28, states that the Services determine a **general area** from information such as IP address and that some Services allow users to **choose to provide more precise device location information**, including GPS-derived location.
2. ChatGPT web-search help states that **device location sharing is optional and off by default**. When enabled, the service may use more specific location for nearby businesses, local news and weather; mobile platforms can expose a separate precise-location control.
3. Current ChatGPT location help says that precise location, when enabled for the described feature, is used to provide a more relevant response and is then deleted rather than retained as precise location linked to the account; location-derived content included in the answer may remain in conversation history.
4. Current ChatGPT Android FAQ states that, unless the user chooses precise location sharing, the Android app does not by default access device Location/Bluetooth/other services to collect or approximate precise location; IP may be used for coarse location.

Primary sources:
- https://openai.com/pt-BR/policies/br-privacy-policy/
- https://help.openai.com/pt-br/articles/9237897-como-pesquisar-na-web-com-o-chatgpt
- https://help.openai.com/pt-br/articles/9237897-pesquisa-do-chatgpt
- https://help.openai.com/en/articles/8142208
- https://openai.com/pt-BR/consumer-privacy/

## 2. What this proves — and what it does not

### VERIFIED at documentation/policy level

- approximate IP-derived location can be used;
- user-enabled device location / precise location is a supported product path;
- precise location sharing is optional rather than a universal always-on input;
- product controls exist for location sharing;
- public documentation describes minimization/retention behavior for precise location in the relevant ChatGPT search path.

### NOT PROVEN by current public documentation

No current public source located in this audit documents that the assistant/model receives raw GNSS engineering telemetry such as:

- constellation + SVID/PRN list;
- visible/tracked/used-in-fix satellite set;
- C/N0 or baseband C/N0;
- azimuth/elevation;
- carrier frequency;
- NMEA sentences;
- pseudorange-related measurements;
- pseudorange rate/Doppler;
- accumulated delta range/carrier-phase-related measurements;
- receiver clock details;
- multipath indicators.

Therefore:

`PRECISE_LOCATION_FEATURE_DOCUMENTED = true`

but

`RAW_GNSS_SATELLITE_TELEMETRY_TO_ASSISTANT_OR_MODEL = TOKEN_VAZIO`

and not `false` unless runtime/product evidence proves absence.

## 3. Semantic separation

`GPS_CHIP_MEASUREMENT`
→ `ANDROID_GNSS_API`
→ `ANDROID_PERMISSION`
→ `CHATGPT_APP_LOCATION_FEATURE`
→ `LOCATION_TOOL_OR_SERVICE`
→ `ASSISTANT_CONTEXT`
→ `MODEL_INPUT`
→ `THIRD_PARTY_LOCAL_PROVIDER_IF_USED`

Each arrow is an independent evidence gate. A policy statement proving one arrow must not be propagated across the entire chain.

## 4. Big Tech responsibility analysis for this product boundary

A legally defensible audit asks:

- Is the field actually collected?
- Is the field needed for the user-selected feature?
- What disclosure/notice is given?
- Which legal basis applies in the user's jurisdiction?
- Is precision granular enough to permit a less intrusive alternative?
- Does the product distinguish coarse location, precise final location and raw GNSS measurements?
- What reaches the model versus a separate local-search/tool provider?
- What is retained and for how long?
- What is shared with third parties and under what minimization/contractual controls?
- Can the user withdraw permission and still use a less precise mode?
- Are UI claims consistent with runtime behavior?

No verified cross-jurisdictional rule found in the parent canon creates a general duty for OpenAI or another Big Tech to expose raw GNSS satellite telemetry to the model. LGPD/GDPR-style necessity and privacy-by-design can point toward **less** collection when raw measurements are not required.

At the same time, if a provider claims a location feature, collects precise location, transfers it, or uses it in ways not accurately described, the relevant privacy, security, consumer-protection and transfer duties remain reviewable.

## 5. Falsifiers

Reject:

- `ChatGPT knows approximate city -> ChatGPT receives GPS satellites`;
- `precise location can be enabled -> raw GNSS is exposed`;
- `raw GNSS is not documented -> raw GNSS definitely never exists in any internal path`;
- `location permission -> unrestricted model access`;
- `privacy minimization -> provider must reveal every sensor field to the AI`.

## 6. TOKEN_VAZIO / next evidence

`TOKEN_VAZIO_RAW_GNSS_RUNTIME` — runtime receipt from an instrumented Android session is required to test whether any raw GNSS field leaves the app/device or enters a ChatGPT location/tool boundary.

`TOKEN_VAZIO_MODEL_CONTEXT_BOUNDARY` — product policy does not itself expose the exact internal boundary between location service/tool processing and model context.

`TOKEN_VAZIO_THIRD_PARTY_LOCATION_PAYLOAD` — public help states trusted third parties may receive minimized location to provide local results; exact per-request payload/provider depends on product implementation and needs request-level evidence.

### F_ok

Public-product location capability, default-off state and coarse-vs-precise distinction are documented.

### F_gap

Raw satellite telemetry, exact model-context injection and request-level third-party payload remain unverified.

### F_next

If runtime verification is authorized and technically available, capture a single controlled Android location request with OS permission state, network destinations, tool invocation boundary and redacted payload schema; do not collect unrelated personal data.