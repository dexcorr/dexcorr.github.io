#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib>=3.10,<4"]
# ///
"""Render the CAD-style training-size geometry figure for the project page."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle


OUTLINE = "#203844"
DIMENSION = "#17678f"
FILL = "#e3e8eb"
INK = "#26343a"
MUTED = "#68757b"
RULE = "#dce3e6"


def center_mark(ax, x: float, y: float) -> None:
    ax.add_patch(Circle((x, y), 3.1, fill=False, edgecolor=OUTLINE, linewidth=1.0))
    ax.add_patch(Circle((x, y), 0.8, color=OUTLINE))


def horizontal_dimension(
    ax,
    x0: float,
    x1: float,
    y: float,
    extension_y: float,
    label: str,
) -> None:
    ax.plot([x0, x0], [extension_y, y + 5], color=DIMENSION, linewidth=0.75)
    ax.plot([x1, x1], [extension_y, y + 5], color=DIMENSION, linewidth=0.75)
    ax.annotate(
        "",
        xy=(x1, y),
        xytext=(x0, y),
        arrowprops={
            "arrowstyle": "<|-|>",
            "color": DIMENSION,
            "linewidth": 0.85,
            "mutation_scale": 5.2,
            "shrinkA": 0,
            "shrinkB": 0,
        },
    )
    ax.text(
        (x0 + x1) / 2,
        y,
        label,
        ha="center",
        va="center",
        color=INK,
        fontsize=10.5,
        bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.6},
    )


def vertical_dimension(
    ax,
    x: float,
    y0: float,
    y1: float,
    extension_x: float,
    label: str,
) -> None:
    ax.plot([extension_x, x - 5], [y0, y0], color=DIMENSION, linewidth=0.75)
    ax.plot([extension_x, x - 5], [y1, y1], color=DIMENSION, linewidth=0.75)
    ax.annotate(
        "",
        xy=(x, y1),
        xytext=(x, y0),
        arrowprops={
            "arrowstyle": "<|-|>",
            "color": DIMENSION,
            "linewidth": 0.85,
            "mutation_scale": 5.2,
            "shrinkA": 0,
            "shrinkB": 0,
        },
    )
    ax.text(
        x + 9,
        (y0 + y1) / 2,
        label,
        ha="left",
        va="center",
        color=INK,
        fontsize=9.3,
    )


def draw_view(
    ax,
    x: float,
    y: float,
    width: float,
    height: float,
    horizontal_label: str | None,
    vertical_label: str | None,
    view_label: str,
) -> None:
    ax.add_patch(
        Rectangle(
            (x, y),
            width,
            height,
            facecolor=FILL,
            edgecolor=OUTLINE,
            linewidth=1.55,
        )
    )
    center_mark(ax, x + width / 2, y + height / 2)
    if horizontal_label:
        horizontal_dimension(ax, x, x + width, y + height + 28, y + height, horizontal_label)
    if vertical_label:
        vertical_dimension(ax, x + width + 28, y, y + height, x + width, vertical_label)
    ax.text(
        x + width / 2,
        y - 14,
        view_label,
        ha="center",
        va="top",
        color=MUTED,
        fontsize=8.5,
        fontweight="bold",
    )


def render(output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "mathtext.fontset": "dejavusans"})

    fig, ax = plt.subplots(figsize=(8.0, 3.0), dpi=220)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(0, 800)
    ax.set_ylim(0, 300)
    ax.set_aspect("equal")
    ax.axis("off")

    # All three views use one common drawing scale: 1 mm = 1.15 plot units.
    scale = 1.15
    length = 150 * scale
    width = 70 * scale
    height = 15 * scale

    draw_view(ax, 45, 142, length, height, None, None, "FRONT")
    draw_view(ax, 310, 108, length, width, "L  150 mm", "W  70 mm", "TOP")
    draw_view(ax, 642, 142, width, height, None, "H  15 mm", "SIDE")

    ax.plot([35, 755], [72, 72], color=RULE, linewidth=0.8)
    ax.text(
        45,
        35,
        "DR RANGE (mm)",
        ha="left",
        va="center",
        color=MUTED,
        fontsize=8.0,
        fontweight="bold",
    )
    for x, label in (
        (285, "L  127.5–172.5"),
        (490, "W  59.5–80.5"),
        (685, "H  12.8–17.2"),
    ):
        ax.text(
            x,
            35,
            label,
            ha="center",
            va="center",
            color=INK,
            fontsize=8.8,
            family="DejaVu Sans Mono",
        )

    fig.savefig(output, bbox_inches="tight", pad_inches=0.08, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    render(Path(__file__).resolve().parents[1] / "static" / "images" / "training-size-geometry.png")
