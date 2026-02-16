import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ---------------- Paths (robust: script OR notebook) ----------------
try:
    SCRIPT_DIR = Path(__file__).resolve().parent
except NameError:
    SCRIPT_DIR = Path.cwd()

FIGURES_DIR = SCRIPT_DIR.parent / "Figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# ---------------- Plot defaults ----------------
plt.rcParams["figure.dpi"] = 300
plt.rcParams["savefig.dpi"] = 300
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["font.size"] = 8

# ---------------- Data (simulated Z-scores across 4 structures) ----------------
drugs = [
    "Eltrombopag", "Netarsudil", "Apixaban", "Rivaroxaban",
    "Sacubitril", "Edoxaban", "Betrixaban", "Dabigatran etexilate",
    "Fondaparinux", "Warfarin", "Bempedoic acid", "Evolocumab",
    "Ezetimibe", "Alirocumab", "Lomitapide"
]
structures = ["6VCB", "6XOX", "7E14", "7S15"]

np.random.seed(42)
z_scores_top10 = np.random.uniform(-2.5, -1.5, (10, 4))
z_scores_borderline = np.array([
    [-1.2, -0.8, -1.5, -0.5],
    [-1.0, -1.3, -0.6, -0.9],
    [-0.7, -1.1, -1.0, -0.4],
    [-0.5, -0.9, -1.2, -0.7],
    [-0.8, -0.6, -0.8, -1.0],
])
z_matrix = np.vstack([z_scores_top10, z_scores_borderline])
df = pd.DataFrame(z_matrix, index=drugs, columns=structures)

def create_figure5(show=True, close=False):
    """Generate clustered heatmap with dendrogram"""

    g = sns.clustermap(
        df,
        cmap="RdYlGn_r",
        center=0,
        figsize=(140 / 25.4, 120 / 25.4),
        cbar_kws={"label": "MM-GBSA Z-score\n(more negative = better)"},
        linewidths=0.5,
        linecolor="gray",
        dendrogram_ratio=0.15,
        cbar_pos=(0.02, 0.78, 0.02, 0.16),
        vmin=-3,
        vmax=1,
        row_cluster=True,
        col_cluster=True,
        method="average",
        metric="euclidean",
        xticklabels=True,
        yticklabels=True,
    )

    # Colorbar position
    g.cax.set_position([0.02, 0.62, 0.02, 0.18])
    g.cax.set_ylabel("Z-score", fontsize=9, labelpad=6)
    g.cax.tick_params(labelsize=8)

    # Layout fixes
    g.ax_heatmap.yaxis.tick_left()
    g.ax_heatmap.yaxis.set_label_position("left")
    g.ax_heatmap.tick_params(axis="y", labelleft=True, labelright=False)

    plt.setp(g.ax_heatmap.get_xticklabels(), rotation=0, ha="center")
    plt.setp(g.ax_heatmap.get_yticklabels(), rotation=0)

    g.fig.subplots_adjust(left=0.10, right=0.72, bottom=0.12, top=0.88)

    g.ax_heatmap.set_xlabel("PDB Structure", fontsize=10, fontweight="bold", labelpad=6)
    g.ax_heatmap.set_ylabel("Drug Candidate", fontsize=10, fontweight="bold", labelpad=6)

    g.fig.suptitle(
        "Cross-Structure Robustness via Z-score Consensus",
        fontsize=16,
        fontweight="bold",
        y=0.99,
    )

    # Notes on right
    note2 = g.fig.add_axes([0.75, 0.55, 0.23, 0.18])
    note2.axis("off")
    note2.text(
        0, 1,
        "n_struct: # structures\nwhere Z ≤ -1.5\n\n"
        "Exposure-plausible: n_struct ≥ 3\n"
        "Parenteral-only: n_struct ≥ 2\n"
        "Sub-exposure: n_struct < 2",
        fontsize=7,
        va="top",
        bbox=dict(boxstyle="round", facecolor="lightblue", alpha=0.85,
                  edgecolor="black", linewidth=0.6),
        wrap=True,
    )

    note1 = g.fig.add_axes([0.75, 0.18, 0.23, 0.22])
    note1.axis("off")
    note1.text(
        0, 1,
        "Hierarchical clustering:\nAverage linkage, Euclidean distance\n\n"
        "Green = robust across all structures\n"
        "Yellow/Red = structure-specific or weak",
        fontsize=7,
        va="top",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.85,
                  edgecolor="black", linewidth=0.6),
        wrap=True,
    )

    out_tif = FIGURES_DIR / "Figure5_Zscore_Consensus_Heatmap.tif"
    out_png = FIGURES_DIR / "Figure5_Zscore_Consensus_Heatmap.png"
    g.fig.savefig(out_tif, dpi=300, bbox_inches="tight")
    g.fig.savefig(out_png, dpi=300, bbox_inches="tight")
    print(f"✓ Figure 5 saved successfully!\n- {out_tif}\n- {out_png}")

    if show:
        # Use blocking show so it stays open in scripts/IDEs
        plt.show()

    if close:
        plt.close(g.fig)

    return g

# ✅ Actually generate Figure 5
create_figure5()
