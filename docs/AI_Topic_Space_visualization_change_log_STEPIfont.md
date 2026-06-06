# AI Topic Space 시각화 변경 기록

Updated: 2026-06-05

## 1. Font Rule Compliance

- Document format: Word `.docx` plus Markdown `.md`.
- Main Korean body font: Noto Serif CJK KR, 10.3pt.
- Heading and auxiliary text font: Noto Sans CJK KR.
- Latin body font: Times New Roman.
- Commercial Daum/Yoon/HY fonts were not detected; Noto fallback fonts were applied.

## 2. Main Changes

- Rebuilt `ai_topic_space_semantic_zoom.html` as a deck.gl semantic zoom browser.
- Kept `ai_topic_space_datamapplot_reference.html` as the pure DatamapPlot reference browser.
- Implemented blended label levels: L0, L0+L1, L1+L2, L2+L3, and L3.
- Made Korea inactive L3 gap nodes the only hover targets in gap mode.
- Added validation snapshots and regenerated manifest.

## 3. Reference Space Counts

| L0         |   L1 |   L2 |   L3 |
|:-----------|-----:|-----:|-----:|
| Policy     |    1 |   23 |  475 |
| Science    |    1 |   35 |  874 |
| Technology |    1 |   17 |  589 |

## 4. Key Files

- Semantic zoom HTML: `/Users/deep1003/data3/ai_knowledge_ecosystem_codex/47_interactive_l1_l2_l3_map/03_html/ai_topic_space_semantic_zoom.html`
- DatamapPlot reference HTML: `/Users/deep1003/data3/ai_knowledge_ecosystem_codex/47_interactive_l1_l2_l3_map/03_html/ai_topic_space_datamapplot_reference.html`
- Payload: `/Users/deep1003/data3/ai_knowledge_ecosystem_codex/47_interactive_l1_l2_l3_map/02_data_outputs/interactive_l1_l2_l3_payload.json`
- Manifest: `/Users/deep1003/data3/ai_knowledge_ecosystem_codex/47_interactive_l1_l2_l3_map/05_logs/semantic_zoom_manifest.json`
- Reference snapshot: `/Users/deep1003/data3/ai_knowledge_ecosystem_codex/47_interactive_l1_l2_l3_map/04_snapshots/ai_topic_space_semantic_zoom_deck_reference_check.png`
- Gap snapshot: `/Users/deep1003/data3/ai_knowledge_ecosystem_codex/47_interactive_l1_l2_l3_map/04_snapshots/ai_topic_space_semantic_zoom_deck_gap_check.png`
