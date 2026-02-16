"""
Figure 1: Pocket Equivalence Across GLP-1R Conformational Ensemble
Generates three panels showing structural conservation and variability
Author: Olaniyi Victor Olaniru
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D

from pathlib import Path

script_dir = Path(__file__).resolve().parent          # .../Python_Scripts
figures_dir = script_dir.parent / "Figures"           # .../Manuscript Files/Figures
figures_dir.mkdir(parents=True, exist_ok=True)


# Set publication-quality defaults
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 8
plt.rcParams['axes.linewidth'] = 0.5

# Data: Grid centers and pocket properties from Table 1
structures = ['6VCB', '6XOX', '7E14', '7S15']
grid_centers = {
    '6VCB': (-151.92, -148.55, -126.52),
    '6XOX': (-152.70, -143.56, -119.74),
    '7E14': (-101.71, -123.91, -79.59),
    '7S15': (-69.81, -69.74, -60.64)
}
pocket_volumes = [465, 390, 385, 345]  # Å³
conserved_waters = [15, 12, 8, 5]
signaling_states = ['PAM-bound\n(GLP-1+PAM)', 'Agonist-bound\n(Gs-coupled)',
                    'Ago-allosteric\n(Gs-coupled)', 'Agonist-bound']

# Color scheme
colors = {'6VCB': '#95A5A6', '6XOX': '#2ECC71', '7E14': '#E74C3C', '7S15': '#3498DB'}

def create_figure1():
    """Generate complete Figure 1 with three panels"""

    fig = plt.figure(figsize=(174/25.4, 60/25.4))  # 174mm wide (double column)

    # Panel B: Pocket volumes
    ax1 = plt.subplot(1, 3, 1)
    bars = ax1.bar(range(len(structures)), pocket_volumes,
                   color=[colors[s] for s in structures],
                   edgecolor='black', linewidth=0.5, alpha=0.8)

    ax1.set_xticks(range(len(structures)))
    ax1.set_xticklabels(structures, fontsize=7)
    ax1.set_ylabel('Pocket Volume (Å³)', fontsize=8)
    ax1.set_xlabel('PDB Structure', fontsize=8)
    ax1.set_title('B. Pocket Volume Variability', fontsize=9, fontweight='bold')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.set_ylim([0, 500])

    # Add value labels on bars
    for i, (bar, vol) in enumerate(zip(bars, pocket_volumes)):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 10,
                f'{vol}',
                ha='center', va='bottom', fontsize=7, fontweight='bold')

    # Add variability annotation
    ax1.axhline(y=np.mean(pocket_volumes), color='gray',
                linestyle='--', linewidth=0.5, alpha=0.5)
    ax1.text(0.5, np.mean(pocket_volumes) + 20,
             f'Mean: {np.mean(pocket_volumes):.0f} Å³\n±{np.std(pocket_volumes):.0f} SD (±{100*np.std(pocket_volumes)/np.mean(pocket_volumes):.0f}%)',
             fontsize=6, ha='left', style='italic', color='gray')

    # Panel C: Grid center clustering (3D)
    ax2 = plt.subplot(1, 3, 2, projection='3d')

    for struct in structures:
        x, y, z = grid_centers[struct]
        ax2.scatter(x, y, z, c=colors[struct], s=100,
                   edgecolors='black', linewidths=0.5,
                   label=struct, alpha=0.8, depthshade=False)

    # Calculate and show RMSD
    coords = np.array([grid_centers[s] for s in structures])
    centroid = coords.mean(axis=0)
    rmsd = np.sqrt(np.mean(np.sum((coords - centroid)**2, axis=1)))

    # Plot centroid
    ax2.scatter(*centroid, c='red', s=200, marker='*',
               edgecolors='black', linewidths=0.5,
               label=f'Centroid\n(RMSD={rmsd:.1f}Å)', depthshade=False)

    # Connect to centroid with lines
    for struct in structures:
        x, y, z = grid_centers[struct]
        ax2.plot([x, centroid[0]], [y, centroid[1]], [z, centroid[2]],
                'k--', linewidth=0.5, alpha=0.3)

    ax2.set_xlabel('X (Å)', fontsize=7, labelpad=2)
    ax2.set_ylabel('Y (Å)', fontsize=7, labelpad=2)
    ax2.set_zlabel('Z (Å)', fontsize=7, labelpad=2)
    ax2.set_title('C. Grid Center Clustering', fontsize=9, fontweight='bold')
    ax2.legend(fontsize=5, loc='upper left', frameon=False)
    ax2.tick_params(labelsize=6, pad=0)
    ax2.view_init(elev=20, azim=45)

    # Panel A: Conserved waters vs volume (correlation analysis)
    ax3 = plt.subplot(1, 3, 3)

    scatter = ax3.scatter(pocket_volumes, conserved_waters,
                         c=[colors[s] for s in structures],
                         s=100, edgecolors='black', linewidths=0.5, alpha=0.8)

    # Add regression line
    z = np.polyfit(pocket_volumes, conserved_waters, 1)
    p = np.poly1d(z)
    x_line = np.linspace(min(pocket_volumes), max(pocket_volumes), 100)
    ax3.plot(x_line, p(x_line), 'k--', linewidth=0.5, alpha=0.5)

    # Calculate R²
    from scipy.stats import pearsonr
    r, pval = pearsonr(pocket_volumes, conserved_waters)

    ax3.text(0.05, 0.95, f'R = {r:.2f}\np = {pval:.3f}',
            transform=ax3.transAxes, fontsize=6,
            verticalalignment='top', bbox=dict(boxstyle='round',
            facecolor='white', alpha=0.8, edgecolor='gray', linewidth=0.5))

    # Add labels for each point
    for i, struct in enumerate(structures):
        ax3.annotate(struct, (pocket_volumes[i], conserved_waters[i]),
                    xytext=(5, 5), textcoords='offset points',
                    fontsize=6, alpha=0.7)

    ax3.set_xlabel('Pocket Volume (Å³)', fontsize=8)
    ax3.set_ylabel('Conserved Waters', fontsize=8)
    ax3.set_title('A. Volume vs. Hydration', fontsize=9, fontweight='bold')
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.grid(True, alpha=0.2, linewidth=0.3)

    plt.tight_layout()
    plt.savefig(figures_dir / "Figure1_Pocket_Equivalence.tif", dpi=300, bbox_inches='tight')
    plt.savefig(figures_dir / "Figure1_Pocket_Equivalence.png", dpi=300, bbox_inches='tight')
    print("✓ Figure 1 saved successfully!")
    plt.show()

if __name__ == "__main__":
    create_figure1()

