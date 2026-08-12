#!/usr/bin/env python3
"""Render the synthetic release-gate comparison as an accessible SVG."""

from __future__ import annotations

import argparse
import csv
import html
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "content/assets/data/evaluation-release-results.csv"
OUTPUT = ROOT / "content/assets/images/evaluation-release-dashboard.svg"


@dataclass(frozen=True)
class Metric:
    name: str
    unit: str
    direction: str
    gate: float
    baseline: float
    candidate: float

    @property
    def passes(self) -> bool:
        if self.direction == "higher":
            return self.candidate >= self.gate
        if self.direction == "lower":
            return self.candidate <= self.gate
        raise ValueError(f"Unsupported direction: {self.direction}")


def load_metrics() -> list[Metric]:
    with SOURCE.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    metrics = [
        Metric(
            name=row["metric"],
            unit=row["unit"],
            direction=row["direction"],
            gate=float(row["gate"]),
            baseline=float(row["baseline"]),
            candidate=float(row["candidate"]),
        )
        for row in rows
    ]
    if not metrics:
        raise ValueError("Evaluation CSV must contain at least one metric")
    return metrics


def display(metric: Metric, value: float) -> str:
    if metric.unit == "rate":
        return f"{value * 100:.0f}%"
    if metric.unit == "seconds":
        return f"{value:.2f}s"
    return f"{value:.2f}"


def render(metrics: list[Metric]) -> str:
    overall = all(metric.passes for metric in metrics)
    width, height = 960, 500
    panel_width = 280
    gap = 24
    start_x = 36
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        "<title id=\"title\">Baseline and candidate release evaluation dashboard</title>",
        "<desc id=\"desc\">Three panels compare answer quality, safety pass rate, and p95 latency. The candidate passes every explicit release gate.</desc>",
        "<rect width=\"960\" height=\"500\" fill=\"#f7faf9\"/>",
        "<text x=\"36\" y=\"52\" font-family=\"system-ui, sans-serif\" font-size=\"28\" font-weight=\"700\" fill=\"#17313b\">Release evaluation</text>",
        "<text x=\"36\" y=\"82\" font-family=\"system-ui, sans-serif\" font-size=\"16\" fill=\"#40545d\">Synthetic example: compare evidence before approving a candidate.</text>",
    ]

    for index, metric in enumerate(metrics):
        x = start_x + index * (panel_width + gap)
        gate_symbol = "&gt;=" if metric.direction == "higher" else "&lt;="
        status = "PASS" if metric.passes else "FAIL"
        status_color = "#137333" if metric.passes else "#b3261e"
        name = html.escape(metric.name)
        parts.extend(
            [
                f'<rect x="{x}" y="116" width="{panel_width}" height="270" rx="6" fill="#ffffff" stroke="#aebdc4"/>',
                f'<text x="{x + 20}" y="154" font-family="system-ui, sans-serif" font-size="18" font-weight="700" fill="#17313b">{name}</text>',
                f'<text x="{x + 20}" y="196" font-family="system-ui, sans-serif" font-size="15" fill="#40545d">Baseline</text>',
                f'<text x="{x + panel_width - 20}" y="196" text-anchor="end" font-family="system-ui, sans-serif" font-size="22" font-weight="700" fill="#40545d">{display(metric, metric.baseline)}</text>',
                f'<text x="{x + 20}" y="244" font-family="system-ui, sans-serif" font-size="15" fill="#40545d">Candidate</text>',
                f'<text x="{x + panel_width - 20}" y="244" text-anchor="end" font-family="system-ui, sans-serif" font-size="22" font-weight="700" fill="#006b5f">{display(metric, metric.candidate)}</text>',
                f'<line x1="{x + 20}" y1="268" x2="{x + panel_width - 20}" y2="268" stroke="#d6e0e4"/>',
                f'<text x="{x + 20}" y="304" font-family="system-ui, sans-serif" font-size="15" fill="#40545d">Gate {gate_symbol} {display(metric, metric.gate)}</text>',
                f'<rect x="{x + 20}" y="326" width="92" height="36" rx="4" fill="{status_color}"/>',
                f'<text x="{x + 66}" y="350" text-anchor="middle" font-family="system-ui, sans-serif" font-size="15" font-weight="700" fill="#ffffff">{status}</text>',
            ]
        )

    overall_text = "RELEASE" if overall else "HOLD"
    overall_color = "#137333" if overall else "#b3261e"
    parts.extend(
        [
            '<text x="36" y="438" font-family="system-ui, sans-serif" font-size="16" font-weight="700" fill="#17313b">Overall gate</text>',
            f'<rect x="158" y="411" width="130" height="40" rx="4" fill="{overall_color}"/>',
            f'<text x="223" y="437" text-anchor="middle" font-family="system-ui, sans-serif" font-size="16" font-weight="700" fill="#ffffff">{overall_text}</text>',
            '<text x="310" y="438" font-family="system-ui, sans-serif" font-size="15" fill="#40545d">All quality, safety, and latency gates must pass.</text>',
            "</svg>",
        ]
    )
    return "\n".join(parts) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail when the generated SVG is stale")
    args = parser.parse_args()
    expected = render(load_metrics())
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != expected:
            print(f"{OUTPUT.relative_to(ROOT)} is stale; run {Path(__file__).name}")
            return 1
        print(f"{OUTPUT.relative_to(ROOT)} is current.")
        return 0
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(expected, encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} from {SOURCE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
