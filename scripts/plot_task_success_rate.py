#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib>=3.10,<4"]
# ///
"""Render the real-world task success-rate figure used on the project page."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib.pyplot as plt


TASKS = ["Flip Cellphone"]
METHODS = {
    "Base": [(0, 10)],
    "ReDex": [(4, 10)],
}


def wilson_interval(successes: int, trials: int, z: float = 1.96) -> tuple[float, float]:
    """Return the Wilson score interval for a binomial proportion."""
    proportion = successes / trials
    denominator = 1 + z**2 / trials
    center = (proportion + z**2 / (2 * trials)) / denominator
    margin = z * math.sqrt(
        proportion * (1 - proportion) / trials + z**2 / (4 * trials**2)
    ) / denominator
    return center - margin, center + margin


def render(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.edgecolor": "#374151",
            "axes.labelcolor": "#374151",
            "xtick.color": "#374151",
            "ytick.color": "#374151",
        }
    )

    fig, ax = plt.subplots(figsize=(6.4, 4.8), dpi=200)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    x_positions = list(range(len(TASKS)))
    bar_width = 0.32
    offsets = {"Base": -bar_width / 1.8, "ReDex": bar_width / 1.8}
    styles = {
        "Base": {"color": "#E5E7EB", "edgecolor": "#374151", "hatch": "///"},
        "ReDex": {"color": "#2563EB", "edgecolor": "#1E3A8A", "hatch": None},
    }

    for method, observations in METHODS.items():
        rates = [successes / trials * 100 for successes, trials in observations]
        intervals = [wilson_interval(successes, trials) for successes, trials in observations]
        lower_errors = [rate - lower * 100 for rate, (lower, _) in zip(rates, intervals)]
        upper_errors = [upper * 100 - rate for rate, (_, upper) in zip(rates, intervals)]
        positions = [x + offsets[method] for x in x_positions]

        bars = ax.bar(
            positions,
            rates,
            width=bar_width,
            label=method,
            linewidth=1.1,
            yerr=[lower_errors, upper_errors],
            capsize=5,
            error_kw={"elinewidth": 1.3, "capthick": 1.3, "ecolor": "#374151"},
            **styles[method],
        )

        for bar, rate, (successes, trials) in zip(bars, rates, observations):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                max(rate + 2.5, 2.5),
                f"{rate:.0f}%\n({successes}/{trials})",
                ha="center",
                va="bottom",
                color="#111827",
                fontsize=10,
                fontweight="bold",
            )

    ax.set_title("Flip Cellphone Success Rate", fontsize=16, fontweight="bold", pad=28)
    ax.text(
        0.5,
        1.02,
        "10 real-world trials per method · 95% Wilson confidence intervals",
        transform=ax.transAxes,
        ha="center",
        va="bottom",
        color="#6B7280",
        fontsize=9.5,
    )
    ax.set_ylabel("Success rate (%)")
    ax.set_xticks(x_positions, TASKS)
    ax.set_ylim(0, 100)
    ax.set_yticks(range(0, 101, 20))
    ax.grid(axis="y", color="#E5E7EB", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(frameon=False, loc="upper right")

    fig.tight_layout()
    for suffix in ("png", "svg"):
        fig.savefig(
            output_dir / f"task-success-rate.{suffix}",
            bbox_inches="tight",
            facecolor="white",
        )
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "static" / "images",
    )
    args = parser.parse_args()
    render(args.output_dir)


if __name__ == "__main__":
    main()
