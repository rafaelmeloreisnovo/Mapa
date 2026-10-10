# AgroGlobal Ω: epistemology, ontology, data semantics

Classes: Commodity, Cultivar, Crop, Harvest, Location, Field, Plot, Source, Quote, MarketVenue, DeliveryPoint, Currency, FXRate, Unit, Transaction, ShippingRoute, Certification, FitosanitaryRequirement, WeatherEvent, YieldEstimate, YieldObservation, IntercroppingSystem, SuccessionSystem, Cost, Claim, Evidence, Receipt.

Typed relations:
Quote --quoted_for--> Commodity; Quote --settled_at--> MarketVenue; Quote --denominated_in--> Currency; Quote --scoped_to--> Grade + Location + Unit + Timestamp.
Harvest --grows--> Crop; Harvest --occurs_in--> Season + Location; Harvest --observed_by--> Source.
Crop --co_planted_with--> Crop (simultaneous consórcio); Crop --succeeded_by--> Crop (sequential safrinha).
Certification --required_by--> ImportMarket [only if regulation/contract supports]; Regulation --valid_from--> Date.
Document --derives_from--> Source (do not equate); Evidence --supports--> Claim [explicit scope].

Epistemic states: SOURCE_OBSERVED, ARTIFACT_CREATED, EXECUTION_OBSERVED, EVIDENCE_VERIFIED, MODELLED_SCENARIO, HYPOTHESIS, TOKEN_VAZIO, CONTRADICTED, NOT_APPLICABLE. Do not map TOKEN_VAZIO to numerical zero.
No causality claim from correlation. No certification guarantee without validating destination law and actual certificate.
Authoritative raw data requires source URL/ID, release/publication time, license, exact bytes and digest, independently of any narrative.
Economics: cash price vs futures vs CIF/FOB vs port export parity; PTAX/market FX quotation type; nominal vs real-adjusted price.
