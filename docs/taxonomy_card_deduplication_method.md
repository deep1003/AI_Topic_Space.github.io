# Taxonomy Card Deduplication Method

This run consolidates model cards whose labels differ only by surface form while preserving domain-specific meanings. Automatic merging is deliberately conservative: two cards are merged only when they belong to the same hierarchy branch and their labels normalize to the same canonical form after removing punctuation, quotation marks, hyphen variants, and simple singular-plural differences.

## Rules

1. STPI topic cards are compared within the same `L0/L1/L2` branch.
2. AI risk cards are compared within the same `L1/L2/L3` branch.
3. Cross-domain and cross-branch cards are not automatically merged, even when they share words.
4. The canonical card preserves the richest definition and evidence metadata; aliases and absorbed IDs are stored as `merged_aliases` and `merged_from_ids`.
5. Korean activation and policy-gap metrics are remapped from duplicate IDs to the canonical ID and numeric masses/counts are aggregated.

## Counts

| Card class | Before | After | Removed |
|---|---:|---:|---:|
| STPI L3 topic cards | 1,938 | 1,930 | 8 |
| AI risk L4 cards | 1,712 | 1,699 | 13 |

## Audit outputs

- Automatic merge audit: `/Users/deep1003/data3/ai_knowledge_ecosystem_codex/48_taxonomy_card_deduplication_20260614/02_outputs/taxonomy_card_deduplication_audit.csv`
- Near-duplicate candidates requiring review: `/Users/deep1003/data3/ai_knowledge_ecosystem_codex/48_taxonomy_card_deduplication_20260614/02_outputs/taxonomy_card_duplicate_candidates_for_review.csv`
- Deduplicated payload: `/Users/deep1003/data3/ai_knowledge_ecosystem_codex/48_taxonomy_card_deduplication_20260614/02_outputs/interactive_l1_l2_l3_payload.deduped.json`
