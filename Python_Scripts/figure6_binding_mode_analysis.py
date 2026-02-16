"""
Figure 6: Binding Mode Analysis - 3D Overlays and 2D Interaction Diagrams
NOTE: This script generates mock 2D interaction fingerprints
3D overlays require PyMOL (see PyMOL_Scripts/figure6_overlays.pml)
Author: Olaniyi Victor Olaniru
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager

# ---------------- Paths (robust) ----------------
# Script directory -> .../Python_Scripts
SCRIPT_DIR = Path(__file__).resolve().parent
# Put Figures next to Python_Scripts (i.e., .../Manuscript Files/Figures)
FIGURES_DIR = SCRIPT_DIR.parent / "Figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

OUT_TIF = FIGURES_DIR / "Figure6_Binding_Mode_Analysis.tif"
OUT_PNG = FIGURES_DIR / "Figure6_Binding_Mode_Analysis.png"

# ---------------- Plot defaults ----------------
plt.rcParams["figure.dpi"] = 300
plt.rcParams["savefig.dpi"] = 300

# Use Arial if installed; otherwise fall back safely.
available_fonts = {f.name for f in font_manager.fontManager.ttflist}
plt.rcParams["font.family"] = "Arial" if "Arial" in available_fonts else "DejaVu Sans"
plt.rcParams["font.size"] = 8

sns.set_style("white")

# ---------------- Data ----------------
key_residues = [
    "R190 (ECL1)", "R227 (TM3)", "Q234 (TM3)", "E387 (TM7)",
    "Y148 (TM2)", "F230 (TM3)", "L384 (TM7)", "L388 (TM7)",
    "W306 (ECL2)", "F324 (ECL2)", "N240 (TM3)"
]

# 1 = interaction present, 0 = absent
interactions = {
    "Eltrombopag": {
        "H-bond donor":     [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
        "H-bond acceptor":  [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        "Pi-Pi stacking":   [0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0],
        "Hydrophobic":      [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
    },
    "Netarsudil": {
        "H-bond donor":     [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        "H-bond acceptor":  [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        "Pi-Pi stacking":   [0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0],
        "Hydrophobic":      [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
    },
    "Apixaban": {
        "H-bond donor":     [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
        "H-bond acceptor":  [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
        "Pi-Pi stacking":   [0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0],
        "Hydrophobic":      [0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0],
    },
}

colors = {"Eltrombopag": "#2ECC71", "Netarsudil": "#3498DB", "Apixaban": "#E74C3C"}


def _validate_inputs():
    """Basic safety checks so mismatched list lengths fail fast."""
    n = len(key_residues)
    for drug, dct in interactions.items():
        for k, v in dct.items():
            if len(v) != n:
                raise ValueError(
                    f"{drug} -> '{k}' has length {len(v)} but key_residues has length {n}."
                )


def create_figure6(show=True):
    """Generate 2D interaction fingerprint heatmaps."""

    _validate_inputs()

    # Larger right margin for the summary textbox
    fig, axes = plt.subplots(
        nrows=3,
        ncols=1,
        figsize=(174 / 25.4, 140 / 25.4),
        sharex=True
    )

    # Keep consistent color scale (0/1)
    vmin, vmax = 0, 1

    for i, (drug, interactions_dict) in enumerate(interactions.items()):
        ax = axes[i]

        # Build DataFrame: rows=residues, cols=interaction types
        df = pd.DataFrame(interactions_dict, index=key_residues)

        # Only show one shared colorbar (first plot)
        cbar = True if i == 0 else False

        hm = sns.heatmap(
            df,
            cmap="YlGnBu",
            vmin=vmin,
            vmax=vmax,
            linewidths=0.5,
            linecolor="white",
            cbar=cbar,
            cbar_kws={"label": "Interaction (0/1)"} if cbar else None,
            ax=ax,
        )

        ax.set_title(
            f"{chr(65 + i)}. {drug} Interaction Fingerprint",
            fontsize=9,
            fontweight="bold",
            color=colors.get(drug, "black"),
            pad=6,
        )
        ax.set_xlabel("Interaction Type", fontsize=8)
        ax.set_ylabel("Key Residue", fontsize=8)
        ax.tick_params(axis="both", labelsize=6)

        # Rotate x-axis labels (only needed on bottom plot, but harmless with sharex)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")

        # Summary counts
        total_interactions = sum(sum(v) for v in interactions_dict.values())
        hbonds = sum(interactions_dict["H-bond donor"]) + sum(interactions_dict["H-bond acceptor"])
        hydrophobic = sum(interactions_dict["Hydrophobic"])
        pi_pi = sum(interactions_dict["Pi-Pi stacking"])

        textstr = (
            f"Total: {total_interactions}\n"
            f"H-bonds: {hbonds}\n"
            f"Hydrophobic: {hydrophobic}\n"
            f"Pi-Pi: {pi_pi}"
        )

        props = dict(
            boxstyle="round",
            facecolor="white",
            alpha=0.92,
            edgecolor=colors.get(drug, "black"),
            linewidth=1,
        )

        # Place summary just to the right of each subplot; keep within figure by expanding right margin
        ax.text(
            1.03,
            0.5,
            textstr,
            transform=ax.transAxes,
            fontsize=6,
            va="center",
            ha="left",
            bbox=props,
        )

    # Leave space on the right for the text boxes
    fig.subplots_adjust(left=0.16, right=0.78, top=0.95, bottom=0.08, hspace=0.35)

    # Save outputs
    fig.savefig(OUT_TIF, dpi=300, bbox_inches="tight")
    fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight")

    print("✓ Figure 6 (2D fingerprints) saved successfully!")
    print(f"  - {OUT_TIF}")
    print(f"  - {OUT_PNG}")
    print("  NOTE: 3D overlays require PyMOL - see PyMOL_Scripts/figure6_overlays.pml")

    if show:
        plt.show()

    return fig


if __name__ == "__main__":
    create_figure6(show=True)
    
