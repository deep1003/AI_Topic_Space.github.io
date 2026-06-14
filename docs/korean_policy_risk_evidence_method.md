# Korean Policy Evidence for AI Risk Cards

## Objective

This module attaches Korean policy-report evidence to the existing L4 AI risk cards. The global English risk definition is preserved. When a risk card is semantically supported by a collected Korean policy document, an additional Korean policy definition, source quote, policy reference, and similarity score are added.

## Inputs

- Korean policy corpus: `/Users/deep1003/data3/ai_knowledge_ecosystem_codex/39_policy_master_v5_integration/02_data_outputs/policy_documents_for_taxonomy_v5_core_only.csv`
- AI risk cards: `/Users/deep1003/data3/AI_Topic_Space.github.io/data/global_ai_risk_l4_overlay_nodes.json`
- Interactive topic-space payload: `/Users/deep1003/data3/AI_Topic_Space.github.io/data/interactive_l1_l2_l3_payload.json`

## Selection Logic

1. Restrict the policy corpus to domestic Korean policy documents.
2. Build an analysis text from title, abstract, keywords, subject classification, document text, and issuing institution.
3. Retain documents that contain at least one AI cue and at least one risk cue.
4. Deduplicate candidate policy documents by year, cleaned Korean title, and cleaned issuing institution.
5. Embed candidate policy texts and L4 risk-card texts with local `bge-m3` through Ollama.
6. Assign a policy document to an L4 risk card when cosine similarity is at least `0.56`.
7. Preserve at most five evidence rows per risk card and use the strongest match as the card-level Korean policy evidence.

## Quote Policy

The preferred quote is an exact sentence from the official abstract when an abstract exists and contains a risk cue. When no such sentence is available, the official Korean title is used as the literal policy-report phrase. The field `source_quote_type` records this distinction:

- `official_abstract_excerpt`: exact excerpt from an official abstract.
- `official_title`: official policy-document title used as the cited phrase.
- `document_text_excerpt`: excerpt from stored document text.
- `policy_text_excerpt`: fallback stored policy text.

Because the collected Korean policy corpus contains few abstracts among the domestic AI-risk candidate documents, most current evidence is title-based. This is recorded explicitly rather than hidden.

## Output Statistics

- Domestic Korean policy documents screened: 4,208
- Candidate Korean AI-risk policy documents after cue filtering and deduplication: 949
- L4 AI risk cards compared: 1,712
- Policy-risk match rows: 2,684
- L4 AI risk cards with Korean policy evidence: 518
- Mean strongest-match similarity: 0.614
- Similarity threshold: 0.56
- Matched period range: 2000-2026

Matched L4 risk cards by L1 family:

| L1 risk family | Matched L4 cards |
|---|---:|
| AI system safety, robustness, and control | 135 |
| Malicious use and weaponization | 82 |
| Socioeconomic and environmental harms | 78 |
| Human agency and interaction harms | 49 |
| Privacy and security harms | 49 |
| Physical AI risks | 46 |
| Discrimination and toxic content | 25 |
| Governance and accountability failures | 24 |
| Agentic and multi-agent system failures | 17 |
| Misinformation and information-ecosystem harms | 10 |
| Cross-cutting harms and trustworthiness failures | 2 |
| Pluralistic value misalignment | 1 |

Quote basis among card-level Korean policy evidence:

| Quote basis | L4 cards |
|---|---:|
| official_title | 517 |
| official_abstract_excerpt | 1 |

## Output Files

- Match table: `/Users/deep1003/data3/ai_risk_coevolution_1990_2026/06_korean_policy_risk_evidence_20260614/02_outputs/korean_policy_ai_risk_l4_matches.csv`
- Enriched risk cards CSV: `/Users/deep1003/data3/ai_risk_coevolution_1990_2026/06_korean_policy_risk_evidence_20260614/02_outputs/global_ai_risk_l4_overlay_nodes.with_korean_policy.csv`
- Enriched risk cards JSON: `/Users/deep1003/data3/ai_risk_coevolution_1990_2026/06_korean_policy_risk_evidence_20260614/02_outputs/global_ai_risk_l4_overlay_nodes.with_korean_policy.json`
- Enriched interactive payload: `/Users/deep1003/data3/ai_risk_coevolution_1990_2026/06_korean_policy_risk_evidence_20260614/02_outputs/interactive_l1_l2_l3_payload.with_korean_policy_risk.json`
- Manifest: `/Users/deep1003/data3/ai_risk_coevolution_1990_2026/06_korean_policy_risk_evidence_20260614/03_logs/korean_policy_risk_evidence_manifest.json`

The synchronized GitHub Pages data files are:

- `/Users/deep1003/data3/AI_Topic_Space.github.io/data/interactive_l1_l2_l3_payload.json`
- `/Users/deep1003/data3/AI_Topic_Space.github.io/data/global_ai_risk_l4_overlay_nodes.json`
- `/Users/deep1003/data3/AI_Topic_Space.github.io/data/global_ai_risk_l4_overlay_nodes.csv`
- `/Users/deep1003/data3/AI_Topic_Space.github.io/data/korean_policy_ai_risk_l4_matches.csv`

## Added Risk-Card Fields

| Field | Meaning |
|---|---|
| `korean_policy_definition` | Korean definition inferred from the matched Korean policy context and the L4 risk label. |
| `korean_policy_quote` | Exact official abstract excerpt when available; otherwise official Korean title. |
| `korean_policy_quote_type` | Provenance type for the quoted phrase. |
| `korean_policy_reference` | Korean citation string: issuing institution, year, title. |
| `korean_policy_reference_title` | Cleaned Korean title. |
| `korean_policy_reference_year` | Publication year. |
| `korean_policy_reference_institution` | Cleaned issuing institution. |
| `korean_policy_reference_url` | Policy source URL or PDF URL when available. |
| `korean_policy_reference_document_id` | Local policy document identifier. |
| `korean_policy_similarity` | BGE-M3 cosine similarity between policy text and L4 risk-card text. |
| `korean_policy_evidence_count` | Number of retained Korean policy evidence rows for that L4 card. |
| `korean_policy_definition_status` | `korean_policy_supported` or `english_only_no_korean_policy_evidence`. |

## Website Integration

The taxonomy browser now displays Korean policy evidence in each supported L4 risk card. The map hover tooltip also includes Korean policy definition, quote, reference, semantic match score, and quote basis when the selected risk card has Korean policy support.

