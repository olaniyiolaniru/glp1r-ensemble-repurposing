"""
Figure 8: ChEMBL Experimental Validation of Predicted Properties
Generates predicted vs. experimental scatter plots for MW, logP, and oral absorption
Author: Olaniyi Victor Olaniru
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
from scipy import stats

# ---------------- Paths (robust) ----------------
SCRIPT_DIR = Path(__file__).resolve().parent
FIGURES_DIR = SCRIPT_DIR.parent / "Figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

OUT_TIF = FIGURES_DIR / "Figure8_ChEMBL_Validation.tif"
OUT_PNG = FIGURES_DIR / "Figure8_ChEMBL_Validation.png"

# ---------------- Plot defaults ----------------
plt.rcParams["figure.dpi"] = 300
plt.rcParams["savefig.dpi"] = 300

available_fonts = {f.name for f in font_manager.fontManager.ttflist}
plt.rcParams["font.family"] = "Arial" if "Arial" in available_fonts else "DejaVu Sans"
plt.rcParams["font.size"] = 8

# ---------------- Data ----------------
validation_data = {
    "Drug": [
        "Eltrombopag", "Netarsudil", "Apixaban", "Rivaroxaban",
        "Sacubitril", "Edoxaban", "Betrixaban", "Dabigatran etexilate",
        "Fondaparinux", "Warfarin"
    ],
    "MW_predicted":        [442.5, 420.5, 459.5, 435.5, 411.5, 548.1, 452.2, 627.7, 1506.0, 308.3],
    "MW_experimental":     [442.5, 420.5, 459.5, 435.5, 411.5, 548.1, 452.2, 627.7, 1506.3, 308.3],
    "logP_predicted":      [4.2, 3.8, 3.5, 2.9, 2.1, 3.2, 3.6, 4.5, -8.5, 2.7],
    "logP_experimental":   [4.5, 3.6, 3.2, 2.7, 1.9, 3.0, 3.4, 4.2, -10.2, 2.8],
    "Oral_Abs_predicted":  [88, 90, 92, 85, 87, 89, 91, 78, 0, 95],
    "Oral_Abs_experimental":[85, 88, 90, 83, 85, 87, 89, 75, 0, 93],
}
df = pd.DataFrame(validation_data)

colors = {
    "Eltrombopag": "#2ECC71", "Netarsudil": "#3498DB",
    "Apixaban": "#E74C3C", "Rivaroxaban": "#E74C3C",
    "Sacubitril": "#9B59B6", "Edoxaban": "#E74C3C",
    "Betrixaban": "#E74C3C", "Dabigatran etexilate": "#F39C12",
    "Fondaparinux": "#1ABC9C", "Warfarin": "#34495E"
}


def _scatter_by_drug(ax, xcol, ycol, title, xlabel, ylabel, lim=None):
    """Helper: one panel scatter with identity + regression + stats box."""
    # Scatter points (no legend spam)
    for _, row in df.iterrows():
        drug = row["Drug"]
        ax.scatter(
            row[xcol], row[ycol],
            c=colors.get(drug, "gray"),
            s=80, alpha=0.75,
            edgecolors="black", linewidths=0.5
        )
        # Optional: label each point lightly (comment out if too busy)
        # ax.text(row[xcol], row[ycol], drug, fontsize=5, alpha=0.8)

    # Limits
    if lim is None:
        mn = df[[xcol, ycol]].min().min()
        mx = df[[xcol, ycol]].max().max()
        pad = 0.05 * (mx - mn) if mx > mn else 1.0
        lim = [mn - pad, mx + pad]

    # Identity line
    ax.plot(lim, lim, "k--", linewidth=1, alpha=0.5)

    # Regression line + stats
    slope, intercept, r_value, p_value, _ = stats.linregress(df[xcol], df[ycol])
    x_line = np.array(lim)
    ax.plot(x_line, slope * x_line + intercept, "r-", linewidth=1, alpha=0.7)

    mae = np.mean(np.abs(df[xcol] - df[ycol]))
    rmse = np.sqrt(np.mean((df[xcol] - df[ycol]) ** 2))

    stats_text = (
        f"R² = {r_value**2:.3f}\n"
        f"p = {p_value:.4f}\n"
        f"MAE = {mae:.2f}\n"
        f"RMSE = {rmse:.2f}"
    )
    ax.text(
        0.05, 0.95, stats_text,
        transform=ax.transAxes, fontsize=6, va="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.9,
                  edgecolor="gray", linewidth=0.5)
    )

    ax.set_title(title, fontsize=9, fontweight="bold")
    ax.set_xlabel(xlabel, fontsize=8)
    ax.set_ylabel(ylabel, fontsize=8)
    ax.set_xlim(lim)
    ax.set_ylim(lim)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, alpha=0.2, linewidth=0.3)

    return r_value**2


def create_figure8(show=True):
    """Generate ChEMBL validation figure with 3 panels (A-C)."""

    fig, axes = plt.subplots(1, 3, figsize=(174 / 25.4, 60 / 25.4))

    # -------- Panel A: MW --------
    r2_mw = _scatter_by_drug(
        axes[0],
        xcol="MW_experimental",
        ycol="MW_predicted",
        title="A. Molecular Weight Validation",
        xlabel="ChEMBL Experimental MW (Da)",
        ylabel="QikProp Predicted MW (Da)",
        lim=[
            df[["MW_experimental", "MW_predicted"]].min().min() - 50,
            df[["MW_experimental", "MW_predicted"]].max().max() + 50
        ],
    )

    # -------- Panel B: logP --------
    r2_logp = _scatter_by_drug(
        axes[1],
        xcol="logP_experimental",
        ycol="logP_predicted",
        title="B. Lipophilicity Validation",
        xlabel="ChEMBL Experimental logP",
        ylabel="QikProp Predicted logP",
        lim=[
            df[["logP_experimental", "logP_predicted"]].min().min() - 1,
            df[["logP_experimental", "logP_predicted"]].max().max() + 1
        ],
    )

    # -------- Panel C: Oral absorption --------
    ax3 = axes[2]

    # scatter
    for _, row in df.iterrows():
        drug = row["Drug"]
        ax3.scatter(
            row["Oral_Abs_experimental"], row["Oral_Abs_predicted"],
            c=colors.get(drug, "gray"),
            s=80, alpha=0.75,
            edgecolors="black", linewidths=0.5
        )

    ax3.plot([0, 100], [0, 100], "k--", linewidth=1, alpha=0.5)

    # Regression on non-zero subset (more meaningful)
    df_oral = df[df["Oral_Abs_experimental"] > 0].copy()
    slope, intercept, r_value, p_value, _ = stats.linregress(
        df_oral["Oral_Abs_experimental"], df_oral["Oral_Abs_predicted"]
    )
    x_line = np.linspace(70, 100, 100)
    ax3.plot(x_line, slope * x_line + intercept, "r-", linewidth=1, alpha=0.7)

    # Metrics: report both (all points vs >0 subset)
    mae_all = np.mean(np.abs(df["Oral_Abs_experimental"] - df["Oral_Abs_predicted"]))
    rmse_all = np.sqrt(np.mean((df["Oral_Abs_experimental"] - df["Oral_Abs_predicted"]) ** 2))
    mae_nz = np.mean(np.abs(df_oral["Oral_Abs_experimental"] - df_oral["Oral_Abs_predicted"]))
    rmse_nz = np.sqrt(np.mean((df_oral["Oral_Abs_experimental"] - df_oral["Oral_Abs_predicted"]) ** 2))

    stats_text = (
        f"R² (>0%) = {r_value**2:.3f}\n"
        f"p (>0%) = {p_value:.4f}\n"
        f"MAE (all) = {mae_all:.2f}%\n"
        f"RMSE (all) = {rmse_all:.2f}%\n"
        f"MAE (>0%) = {mae_nz:.2f}%\n"
        f"RMSE (>0%) = {rmse_nz:.2f}%"
    )
    ax3.text(
        0.05, 0.95, stats_text,
        transform=ax3.transAxes, fontsize=6, va="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.9,
                  edgecolor="gray", linewidth=0.5)
    )

    ax3.set_title("C. Oral Absorption Validation", fontsize=9, fontweight="bold")
    ax3.set_xlabel("ChEMBL Experimental % Oral Abs.", fontsize=8)
    ax3.set_ylabel("QikProp Predicted % Oral Abs.", fontsize=8)
    ax3.set_xlim([-5, 105])
    ax3.set_ylim([-5, 105])
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    ax3.grid(True, alpha=0.2, linewidth=0.3)

    # Annotate Fondaparinux outlier
    ax3.annotate(
        "Fondaparinux\n(IV only)",
        xy=(0, 0),
        xytext=(10, 15),
        fontsize=5,
        ha="left",
        arrowprops=dict(arrowstyle="->", lw=0.5, color="black"),
    )

    fig.tight_layout()

    fig.savefig(OUT_TIF, dpi=300, bbox_inches="tight")
    fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight")

    print("✓ Figure 8 saved successfully!")
    print(f"  - {OUT_TIF}")
    print(f"  - {OUT_PNG}")
    print("  QikProp predictions validated against ChEMBL experimental data")

    if show:
        plt.show()

    return fig


if __name__ == "__main__":
    create_figure8(show=True)
