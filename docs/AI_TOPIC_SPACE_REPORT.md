# AI Topic Space L0/L1/L2/L3 Report

Updated: 2026-06-05

## Purpose

This module records the current AI Topic Space visualization and reporting layer used in the manuscript and Appendix A. The purpose is to make the hierarchy, activation logic, policy-gap definition, HTML artifact, static snapshots, and LaTeX integration auditable from one local folder.

## Four-Level Classification

- **L0**: analytical domain. The current domains are `Policy`, `Science`, and `Technology`.
- **L1**: broad thematic family within each L0 domain. The final L1 labels are `AI policy and governance`, `AI science and research`, and `AI technology and invention`.
- **L2**: intermediate semantic cluster within L1. L2 labels were assigned after embedding-space clustering and researcher-intervention review.
- **L3**: finest-grained key phrase node. Documents are mapped to L3 terms, and activation, entropy, coverage, and gap statistics are computed at L3 before aggregation.

## Reference-Space Counts

| L0 | L1 count | L2 count | L3 count |
|---|---:|---:|---:|
| Policy | 1 | 23 | 475 |
| Science | 1 | 35 | 874 |
| Technology | 1 | 17 | 589 |

The total dictionary-defined reference space contains 1,938 L3 nodes. These counts are denominators, not observed Korean activations.

## View Modes

1. **Reference L0/L1/L2/L3 space**: period-invariant dictionary reference space.
2. **Korea activation**: Korean papers, policy reports, and patents activated on top of the reference space. Marker size scales by fractional activation mass.
3. **Korea inactive L3 (gap)**: L3 nodes activated in the global policy corpus but not activated by Korean policy reports under a selected period and corpus filter.

## Interactive Semantic-Zoom Layer

Two additional browser artifacts were added to support an Alammar/DatamapPlot-style reading of the AI Topic Space.

- `03_html/ai_topic_space_datamapplot_reference.html` is a pure DatamapPlot reference browser. It passes four ordered label layers to `datamapplot.create_interactive_plot`: L3, L2, L1, and L0. This file is useful for inspecting the period-invariant reference denominator and topic-tree behavior without Korean activation overlays.
- `03_html/ai_topic_space_semantic_zoom.html` is a deck.gl semantic-zoom browser built from the same payload. It keeps L3 key phrases as final nodes, colors nodes by L2 cluster within the Policy, Science, and Technology domains, and changes overlay labels as the user zooms. The label transition is intentionally blended: full scale shows L0 labels, early zoom shows L0+L1, middle zoom shows L1+L2, local zoom shows L2+representative L3, and close zoom prioritizes selected L3 key phrases. This makes local representative labels visible before the user fully zooms into a region. The design avoids the leader-line label style used in static figures while preserving exact node-level metadata through hover.

The semantic-zoom version retains the three view modes above. In Korea activation mode, marker size scales with fractional activation mass. In Korea inactive L3 mode, inactive nodes are marked with an open-circle plus an x overlay; non-gap background nodes remain muted and are not hover targets.

## Document-to-L3 Activation Rule

For each document, candidate L3 links are retained when:

- the candidate is within the domain-specific top 5 nearest L3 phrases;
- cosine similarity is at least 0.50;
- the similarity gap from the document's top-1 L3 is at most 0.10.

If more than one L3 is retained, the document is fractionally weighted by relative cosine similarity. A corpus-period L3 node is treated as activated when the summed fractional activation mass is greater than zero.

For policy gaps, an L3 is counted as a Korea inactive L3 when it is activated in the global policy corpus for the selected period but has zero Korean policy activation mass in that same period.

## Main Artifacts

- HTML: `03_html/ai_knowledge_l1_l2_l3_interactive_map.html`
- Semantic zoom HTML: `03_html/ai_topic_space_semantic_zoom.html`
- DatamapPlot reference HTML: `03_html/ai_topic_space_datamapplot_reference.html`
- Payload: `02_data_outputs/interactive_l1_l2_l3_payload.json`
- Hierarchy counts: `02_data_outputs/l0_l1_l2_l3_hierarchy_counts.csv`
- Representative examples: `02_data_outputs/l0_l1_l2_l3_representative_examples.csv`
- L2 cluster counts: `02_data_outputs/l0_l1_l2_cluster_counts.csv`
- Full L3 dictionary: `02_data_outputs/l0_l1_l2_l3_dictionary_for_appendix.csv`
- Snapshot manifest: `02_data_outputs/ai_topic_space_snapshot_manifest.json`

## Static Snapshot Figures

- `04_snapshots/ai_topic_space_reference_l0_l1_l2_l3.png`
- `04_snapshots/ai_topic_space_korea_activation_2022_2026.png`
- `04_snapshots/ai_topic_space_korea_policy_gap_2022_2026.png`
- `04_snapshots/ai_topic_space_semantic_zoom_browser_check.png`

The snapshots are generated from the same JSON payload used by the HTML browser, so manuscript figures and the interactive artifact share the same coordinates, hierarchy labels, and activation/gap states.

## Scripts

- `01_scripts/build_interactive_l1_l2_l3_map.py`: builds the standalone interactive HTML and embedded payload.
- `01_scripts/build_ai_topic_space_snapshots.py`: builds hierarchy audit tables and publication-style static snapshots.
- `01_scripts/build_semantic_zoom_ai_topic_space.py`: builds the DatamapPlot reference HTML and the custom semantic-zoom HTML.

## Manuscript Integration

The current manuscript integration was made in:

- `/Users/deep1003/Library/CloudStorage/OneDrive-개인/data1/ai_korea_literature_1990_2026/TFSC_LaTeX_submission/body.tex`
- `/Users/deep1003/Library/CloudStorage/OneDrive-개인/data1/ai_korea_literature_1990_2026/TFSC_LaTeX_submission/appendix_a.tex`

The LaTeX manuscript now explicitly defines L0/L1/L2/L3 in the methods, reports L0-level counts in the results, and includes static AI Topic Space snapshots in the body and appendix.

## Review Notes

- Claude stats-reviewer call failed due to a local certificate/API connection error.
- Gemini code review returned generic reproducibility checks; LaTeX compilation verified that figure paths are valid.
- Gemini stats-reviewer recommended explicitly stating the activation threshold, clarifying the Korea inactive L3 gap ratio, and noting possible global policy reference-corpus source bias. These points were incorporated into `appendix_a.tex`, `body.tex`, and this report.
