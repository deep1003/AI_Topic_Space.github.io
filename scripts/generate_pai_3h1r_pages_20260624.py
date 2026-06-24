#!/usr/bin/env python3
"""Generate static Physical AI 3H1R taxonomy pages from payload JSON."""

from __future__ import annotations

import html
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / "data" / "interactive_l1_l2_l3_payload.json"
V7_OUT = ROOT / "pages" / "pai_risk_taxonomy_bilingual_v7.html"
RATIONALE_OUT = ROOT / "pages" / "pai_3h1r_rationale_20260624.html"

BADGE_COLORS = {
    ("H1", "P"): ("#e8f5e9", "#2e7d32", "#a5d6a7"),
    ("H2", "P"): ("#fce4ec", "#b71c1c", "#ef9a9a"),
    ("H3", "P"): ("#fff3e0", "#e65100", "#ffcc80"),
    ("RC", "P"): ("#ede7f6", "#4527a0", "#b39ddb"),
    ("H1", "S"): ("#e8f4fd", "#1565c0", "#90caf9"),
    ("H2", "S"): ("#fdecea", "#c62828", "#ef9a9a"),
    ("H3", "S"): ("#fff8e1", "#f57c00", "#ffe082"),
    ("RC", "S"): ("#ede7f6", "#6a1b9a", "#ce93d8"),
}

PREFIX_LABEL = {
    "PHYSBENCH": "Benchmark / Evaluation",
    "PHYSRISK": "Physical Risk",
    "PHYSCONN": "Connectivity Risk",
    "PHYSKR": "Korea-specific Risk",
}


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def load_cards() -> list[dict]:
    data = json.loads(PAYLOAD.read_text(encoding="utf-8"))
    cards = [r for r in data["risk_nodes"] if str(r.get("id", "")).startswith("PHYS")]
    return sorted(cards, key=lambda r: (str(r.get("id", "")).split("-")[0], str(r.get("l2", "")), str(r.get("l3", "")), str(r.get("id", ""))))


def prefix(card: dict) -> str:
    return str(card.get("id", "")).split("-")[0]


def badge(dim: str, val: str) -> str:
    if val not in {"P", "S"}:
        return ""
    bg, color, border = BADGE_COLORS[(dim, val)]
    return f'<span class="hhh-badge" style="background:{bg};color:{color};border-color:{border}">{dim}·{val}</span>'


def card_badges(card: dict) -> str:
    parts = []
    for dim, key in [
        ("H1", "alignment_3h1r_h1"),
        ("H2", "alignment_3h1r_h2"),
        ("H3", "alignment_3h1r_h3"),
        ("RC", "alignment_3h1r_rc"),
    ]:
        b = badge(dim, str(card.get(key, "")).strip())
        if b:
            parts.append(b)
    return "".join(parts)


def evidence_link(card: dict) -> str:
    url = card.get("evidence_url_v5") or card.get("evidence_url") or ""
    title = card.get("evidence_title_v5") or card.get("evidence_title") or ""
    if not url:
        return '<span class="src-na">No evidence URL</span>'
    return f'<a class="src-link" href="{esc(url)}" target="_blank" rel="noopener">{esc(title or url)}</a>'


def physbench_link(card: dict) -> str:
    if not card.get("physbench_reference_url"):
        return ""
    tier = card.get("physbench_relevance_tier", "")
    title = card.get("physbench_reference_title", "PhysBench")
    url = card.get("physbench_reference_url")
    return (
        '<div class="source physbench-ref">'
        f'<span>PhysBench {esc(tier)}</span>'
        f'<a class="src-link" href="{esc(url)}" target="_blank" rel="noopener">{esc(title)}</a>'
        "</div>"
    )


def render_v7(cards: list[dict]) -> str:
    counts = Counter(prefix(c) for c in cards)
    l2_counts = Counter(c.get("l2", "Unspecified") for c in cards)
    l3_counts = Counter(c.get("l3", "Unspecified") for c in cards)
    cards_by_l2: dict[str, list[dict]] = defaultdict(list)
    for card in cards:
        cards_by_l2[str(card.get("l2", "Unspecified"))].append(card)

    legend = "".join(badge(dim, val) for dim in ["H1", "H2", "H3", "RC"] for val in ["P", "S"])
    tabs = "\n".join(
        f'<button class="tab" data-prefix="{p}" onclick="filterPrefix(\'{p}\')">{p} <span>{counts[p]}</span></button>'
        for p in ["PHYSBENCH", "PHYSRISK", "PHYSCONN", "PHYSKR"]
    )
    sections = []
    for l2, l2_cards in cards_by_l2.items():
        by_l3: dict[str, list[dict]] = defaultdict(list)
        for card in l2_cards:
            by_l3[str(card.get("l3", "Unspecified"))].append(card)
        l3_blocks = []
        for l3, group_cards in by_l3.items():
            card_html = []
            for card in group_cards:
                pfx = prefix(card)
                primary = esc(card.get("alignment_3h1r_primary", ""))
                secondary = esc(card.get("alignment_3h1r_secondary", ""))
                card_html.append(
                    f"""
<article class="risk-card" data-prefix="{esc(pfx)}" data-id="{esc(card.get('id'))}">
  <div class="card-top"><span class="id">{esc(card.get('id'))}</span><span class="prefix">{esc(PREFIX_LABEL.get(pfx, pfx))}</span></div>
  <h4>{esc(card.get('l4_label'))}</h4>
  <div class="ko">{esc(card.get('korean_label'))}</div>
  <p>{esc(card.get('definition'))}</p>
  <p class="korean-def">{esc(card.get('korean_definition'))}</p>
  <div class="hhh-bar">{card_badges(card)}</div>
  <div class="align-meta">Primary: {primary or '—'} · Secondary: {secondary or '—'}</div>
  <div class="source">{evidence_link(card)}</div>
  {physbench_link(card)}
</article>"""
                )
            l3_blocks.append(
                f"""
<details open class="l3-block">
  <summary>{esc(l3)} <span>{len(group_cards)}</span></summary>
  <div class="cards-grid">{''.join(card_html)}</div>
</details>"""
            )
        sections.append(
            f"""
<section class="l2-section">
  <h2>{esc(l2)} <span>{len(l2_cards)}</span></h2>
  {''.join(l3_blocks)}
</section>"""
        )

    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>PAI Risk Taxonomy v7 | Physical AI Risk L4 카드 + 3H1R 정렬</title>
<style>
*{{box-sizing:border-box}} body{{margin:0;background:#f7f8fb;color:#172033;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;font-size:14px}}
header{{background:#111827;color:white;padding:26px 32px 20px}} h1{{margin:0 0 8px;font-size:24px}} header p{{margin:0;color:#cbd5e1}}
.toolbar{{position:sticky;top:0;z-index:20;background:white;border-bottom:1px solid #e5e7eb;padding:12px 32px;display:flex;gap:8px;flex-wrap:wrap;align-items:center}}
.tab,.tool{{border:1px solid #d1d5db;background:#f9fafb;border-radius:7px;padding:7px 11px;cursor:pointer;font-weight:650}} .tab.active,.tool:hover{{background:#111827;color:white}} .tab span{{font-size:12px;color:#64748b;margin-left:4px}} .tab.active span{{color:#e5e7eb}}
.search{{border:1px solid #d1d5db;border-radius:7px;padding:8px 10px;min-width:260px}}
.hhh-legend{{display:flex;gap:7px;flex-wrap:wrap;align-items:center;background:#fff7ed;border-bottom:1px solid #fed7aa;padding:10px 32px}} .legend-title{{font-weight:800;color:#7c2d12;margin-right:6px}}
.hhh-badge{{display:inline-flex;align-items:center;justify-content:center;border:1.5px solid;border-radius:999px;padding:2px 8px;font-size:11px;font-weight:800;line-height:1.35;margin-right:5px;margin-bottom:4px}}
main{{max-width:1440px;margin:0 auto;padding:24px 32px 40px}} .kpis{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-bottom:20px}} .kpi{{background:white;border:1px solid #e5e7eb;border-radius:8px;padding:14px 16px}} .kpi b{{display:block;font-size:26px;margin-bottom:4px}} .kpi span{{color:#64748b;font-size:12px}}
.l2-section{{margin:22px 0;background:white;border:1px solid #e5e7eb;border-radius:10px;overflow:hidden}} .l2-section h2{{margin:0;padding:14px 18px;background:#f1f5f9;font-size:17px}} .l2-section h2 span{{font-size:12px;background:#111827;color:white;border-radius:999px;padding:2px 8px;margin-left:8px}}
.l3-block{{border-top:1px solid #e5e7eb}} .l3-block summary{{cursor:pointer;padding:12px 18px;font-weight:750}} .l3-block summary span{{font-size:12px;color:#64748b;margin-left:6px}}
.cards-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:12px;padding:0 18px 18px}} .risk-card{{border:1px solid #e5e7eb;border-radius:8px;background:#fcfcfd;padding:12px;min-height:245px}} .card-top{{display:flex;justify-content:space-between;gap:8px;align-items:center;margin-bottom:8px}} .id{{font-size:11px;font-weight:800;color:#1d4ed8}} .prefix{{font-size:10px;color:#64748b;background:#eef2ff;border-radius:999px;padding:2px 7px;white-space:nowrap}}
.risk-card h4{{font-size:14px;line-height:1.35;margin:0 0 4px}} .ko{{font-size:12px;font-weight:700;color:#334155;margin-bottom:8px}} .risk-card p{{font-size:12px;line-height:1.45;color:#475569;margin:0 0 8px}} .korean-def{{color:#64748b!important}} .hhh-bar{{min-height:24px;margin:8px 0}} .align-meta{{font-size:11px;color:#64748b;margin-bottom:8px}} .source{{margin-top:5px}} .src-link{{font-size:11px;color:#0369a1;text-decoration:none}} .src-link:hover{{text-decoration:underline}} .src-na{{font-size:11px;color:#94a3b8}} .physbench-ref span{{display:inline-block;font-size:10px;font-weight:800;color:#7c2d12;background:#ffedd5;border-radius:999px;padding:2px 6px;margin-right:6px}}
@media(max-width:800px){{.kpis{{grid-template-columns:repeat(2,1fr)}} header,.toolbar,.hhh-legend,main{{padding-left:16px;padding-right:16px}}}}
</style>
</head>
<body>
<header>
  <h1>PAI Risk Taxonomy v7 | Physical AI Risk L4 카드 + 3H1R 정렬</h1>
  <p>ASIMOV v2 기준 · 182개 L4 카드 · 3H1R 정렬 마킹 통합 (2026-06-24) · {len(l2_counts)}개 L2 · {len(l3_counts)}개 L3</p>
</header>
<nav class="toolbar">
  <button class="tab active" onclick="filterPrefix('ALL')">전체 <span>{len(cards)}</span></button>
  {tabs}
  <input class="search" id="q" oninput="filterText()" placeholder="카드 ID, L4, 정의 검색">
  <button class="tool" onclick="expandAll()">전체 펼치기</button>
  <button class="tool" onclick="collapseAll()">전체 접기</button>
</nav>
<div class="hhh-legend"><span class="legend-title">3H1R legend</span>{legend}<span style="color:#9a3412;font-size:12px">P=Primary, S=Secondary</span></div>
<main>
<div class="kpis">
  <div class="kpi"><b>{len(cards)}</b><span>Total L4 cards</span></div>
  <div class="kpi"><b>{len(l3_counts)}</b><span>L3 groups</span></div>
  <div class="kpi"><b>{sum(1 for c in cards if c.get('alignment_3h1r_primary'))}</b><span>Cards with Primary</span></div>
  <div class="kpi"><b>PHYSRISK×{counts['PHYSRISK']} · PHYSBENCH×{counts['PHYSBENCH']} · PHYSCONN×{counts['PHYSCONN']} · PHYSKR×{counts['PHYSKR']}</b><span>Source groups</span></div>
</div>
{''.join(sections)}
</main>
<script>
let activePrefix='ALL';
function filterPrefix(prefix){{activePrefix=prefix;document.querySelectorAll('.tab').forEach(b=>b.classList.toggle('active',b.dataset.prefix===prefix||(prefix==='ALL'&&!b.dataset.prefix)));filterText();}}
function filterText(){{const q=(document.getElementById('q').value||'').toLowerCase();document.querySelectorAll('.risk-card').forEach(card=>{{const prefixOk=activePrefix==='ALL'||card.dataset.prefix===activePrefix;const textOk=!q||card.textContent.toLowerCase().includes(q);card.style.display=(prefixOk&&textOk)?'block':'none';}});}}
function expandAll(){{document.querySelectorAll('details').forEach(d=>d.open=true);}}
function collapseAll(){{document.querySelectorAll('details').forEach(d=>d.open=false);}}
</script>
</body>
</html>
"""


def rationale_text(card: dict) -> str:
    primary = [x.strip() for x in str(card.get("alignment_3h1r_primary", "")).split(",") if x.strip()]
    secondary = [x.strip() for x in str(card.get("alignment_3h1r_secondary", "")).split(",") if x.strip()]
    label = card.get("l4_label") or card.get("korean_label") or card.get("id")
    p = ", ".join(primary) if primary else "없음"
    s = ", ".join(secondary) if secondary else "없음"
    return f"{esc(label)} 카드의 직접 실패 메커니즘은 {esc(p)}로 정렬되며, 보조적 기여 또는 하류 결과는 {esc(s)}로 표시했다."


def cell(dim: str, card: dict) -> str:
    key = {"H1": "alignment_3h1r_h1", "H2": "alignment_3h1r_h2", "H3": "alignment_3h1r_h3", "RC": "alignment_3h1r_rc"}[dim]
    value = str(card.get(key, "")).strip()
    return badge(dim, value) if value else '<span class="dash">—</span>'


def physbench_cell(card: dict) -> str:
    if not card.get("physbench_reference_url"):
        return '<span class="dash">—</span>'
    tier = card.get("physbench_relevance_tier", "")
    return (
        f'<a class="src-link" href="{esc(card.get("physbench_reference_url"))}" target="_blank" rel="noopener">PhysBench</a>'
        f'<br><span class="tier">{esc(tier)}</span>'
    )


def render_rationale(cards: list[dict]) -> str:
    counts = Counter()
    for card in cards:
        for dim, key in [("H1", "alignment_3h1r_h1"), ("H2", "alignment_3h1r_h2"), ("H3", "alignment_3h1r_h3"), ("RC", "alignment_3h1r_rc")]:
            if card.get(key) == "P":
                counts[dim] += 1
    rows = []
    last_group = None
    for card in cards:
        group = f"{prefix(card)} — {card.get('l3', 'Unspecified')}"
        if group != last_group:
            rows.append(f'<tr class="group"><td colspan="8">{esc(group)}</td></tr>')
            last_group = group
        rows.append(
            f"""
<tr>
  <td>{esc(card.get('l3'))}</td>
  <td><span class="id">{esc(card.get('id'))}</span><br><b>{esc(card.get('korean_label'))}</b><br><span class="en">{esc(card.get('l4_label'))}</span></td>
  <td>{cell('H1', card)}</td>
  <td>{cell('H2', card)}</td>
  <td>{cell('H3', card)}</td>
  <td>{cell('RC', card)}</td>
  <td>{physbench_cell(card)}</td>
  <td class="why">{rationale_text(card)}</td>
</tr>"""
        )
    legend = "".join(badge(dim, val) for dim in ["H1", "H2", "H3", "RC"] for val in ["P", "S"])
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Physical AI Risk Taxonomy — 3H1R 적용</title>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;margin:0;padding:24px 32px;background:#f8f9fb;color:#111827}}
h1{{font-size:23px;margin:0 0 4px}} .sub{{color:#64748b;margin:0 0 18px}} .legend,.stats{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px;align-items:center}} .stat{{background:white;border:1px solid #e5e7eb;border-radius:8px;padding:10px 14px;font-size:12px}} .stat b{{display:block;font-size:20px}}
.hhh-badge{{display:inline-flex;align-items:center;justify-content:center;border:1.5px solid;border-radius:999px;padding:2px 8px;font-size:11px;font-weight:800;line-height:1.35;margin:1px}}
table{{width:100%;border-collapse:collapse;background:white;border:1px solid #e5e7eb;border-radius:10px;overflow:hidden}} th{{position:sticky;top:0;background:#eef2f7;font-size:12px;text-align:left;padding:9px;border-bottom:1px solid #cbd5e1;z-index:1}} td{{border-bottom:1px solid #eef2f7;padding:8px;vertical-align:middle;font-size:12px;line-height:1.45}} td:nth-child(3),td:nth-child(4),td:nth-child(5),td:nth-child(6){{text-align:center;white-space:nowrap}} .group td{{background:#e0f2fe;color:#075985;font-weight:800;border-top:2px solid #bae6fd}} .id{{font-size:11px;color:#1d4ed8;font-weight:800}} .en{{color:#64748b;font-size:11px}} .dash{{color:#94a3b8}} .why{{color:#334155}} .src-link{{font-size:11px;color:#0369a1;text-decoration:none}} .src-link:hover{{text-decoration:underline}} .tier{{display:inline-block;margin-top:3px;font-size:10px;font-weight:800;color:#7c2d12;background:#ffedd5;border-radius:999px;padding:2px 6px}}
</style>
</head>
<body>
<h1>Physical AI Risk Taxonomy — 3H1R 적용</h1>
<p class="sub">182개 L4 리스크 카드 대상</p>
<div class="legend"><b>Legend</b>{legend}</div>
<div class="stats">
  <div class="stat"><b>{counts['H1']}</b>H1 Primary</div>
  <div class="stat"><b>{counts['H2']}</b>H2 Primary</div>
  <div class="stat"><b>{counts['H3']}</b>H3 Primary</div>
  <div class="stat"><b>{counts['RC']}</b>RC Primary</div>
  <div class="stat"><b>{len(cards)}</b>전체 카드</div>
</div>
<table>
<thead><tr><th style="width:14%">L3 그룹</th><th style="width:20%">L4 카드명</th><th>H1<br>Helpful</th><th>H2<br>Harmless</th><th>H3<br>Honest</th><th>RC</th><th>PhysBench</th><th>판단근거</th></tr></thead>
<tbody>{''.join(rows)}</tbody>
</table>
</body>
</html>
"""


def main() -> None:
    cards = load_cards()
    if len(cards) != 182:
        raise SystemExit(f"Expected 182 PHYS cards, got {len(cards)}")
    missing = [c["id"] for c in cards if not c.get("alignment_3h1r_primary")]
    if missing:
        raise SystemExit(f"Cards missing primary alignment: {missing[:5]}")
    V7_OUT.write_text("\n".join(line.rstrip() for line in render_v7(cards).splitlines()) + "\n", encoding="utf-8")
    RATIONALE_OUT.write_text("\n".join(line.rstrip() for line in render_rationale(cards).splitlines()) + "\n", encoding="utf-8")
    print(f"Wrote {V7_OUT} and {RATIONALE_OUT}")


if __name__ == "__main__":
    main()
