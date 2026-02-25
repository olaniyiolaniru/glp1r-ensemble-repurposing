# Data Availability Statement

## Overview
This folder contains raw computational data supporting the manuscript:

**"Computational Repurposing Screen Identifies Oral Drug Candidates for GLP-1 Receptor Modulation"**

## ⚠️ Data Location

Due to file size limitations, all raw data files are deposited externally:

### Zenodo Repository

Software (code snapshot): 10.5281/zenodo.18771750
Dataset (Supplementary_Data.zip): 10.5281/zenodo.18682381

---

## 📁 Deposited Files

### 1. Protein Structures (Prepared for Docking)

| File                    | Description                              | Size  |
|-------------------------|------------------------------------------|-------|
| `6VCB_prepared.pdb`     | PAM-bound GLP-1R (prepared, pH 7.4)     | 2.1 MB|
| `6XOX_prepared.pdb`     | Agonist-bound GLP-1R (Gs-coupled)       | 2.3 MB|
| `7E14_prepared.pdb`     | Ago-allosteric GLP-1R (Gs-coupled)      | 2.2 MB|
| `7S15_prepared.pdb`     | Agonist-bound GLP-1R (reference)        | 2.4 MB|

**Preparation Protocol:**
- Schrödinger Protein Preparation Wizard
- PROPKA pH 7.4
- OPLS4 force field
- Minimization: RMSD < 0.30 Å

---

### 2. Docking Grids

| File                    | Description                              | Size   |
|-------------------------|------------------------------------------|--------|
| `6VCB_grid.zip`         | Glide XP docking grid (orforglipron pocket) | 45 MB |
| `6XOX_grid.zip`         | Glide XP docking grid                    | 48 MB  |
| `7E14_grid.zip`         | Glide XP docking grid                    | 46 MB  |
| `7S15_grid.zip`         | Glide XP docking grid                    | 47 MB  |

**Grid Parameters:**
- Grid center coordinates (see Table 1 in manuscript)
- Inner box: 10 × 10 × 10 Å
- Outer box: 30 × 30 × 30 Å
- Van der Waals scaling: 1.0 (receptor), 0.8 (ligand)

---

### 3. Glide Docking Input Files

| File                          | Description                        | Size  |
|-------------------------------|------------------------------------|-------|
| `glide_xp_input_6VCB.in`      | Glide XP settings (6VCB)          | 2 KB  |
| `glide_xp_input_6XOX.in`      | Glide XP settings (6XOX)          | 2 KB  |
| `glide_xp_input_7E14.in`      | Glide XP settings (7E14)          | 2 KB  |
| `glide_xp_input_7S15.in`      | Glide XP settings (7S15)          | 2 KB  |

**Key Settings:**
- Precision: XP (Extra Precision)
- Poses per ligand: 5
- Energy window: 100 kcal/mol
- Pose RMSD: 0.5 Å

---

### 4. Top-Ranked Docking Poses

| File                                | Description                              | Size   |
|-------------------------------------|------------------------------------------|--------|
| `eltrombopag_7S15_top_pose.sdf`     | Rank 1 pose (ΔG = -78.5 kcal/mol)       | 5 KB   |
| `netarsudil_7E14_top_pose.sdf`      | Rank 1 pose (ΔG = -75.2 kcal/mol)       | 5 KB   |
| `apixaban_6XOX_top_pose.sdf`        | Rank 1 pose (ΔG = -73.8 kcal/mol)       | 5 KB   |
| `all_top_poses_6VCB.sdf`            | Top 50 poses (MM-GBSA rescored)         | 250 KB |
| `all_top_poses_6XOX.sdf`            | Top 50 poses (MM-GBSA rescored)         | 255 KB |
| `all_top_poses_7E14.sdf`            | Top 50 poses (MM-GBSA rescored)         | 260 KB |
| `all_top_poses_7S15.sdf`            | Top 50 poses (MM-GBSA rescored)         | 240 KB |

---

### 5. Complete Docking Results (CSV)

| File                                  | Description                        | Size   |
|---------------------------------------|------------------------------------|--------|
| `docking_results_all_structures.csv`  | N=8,472 (2,118 drugs × 4 structures)| 1.2 MB |

**Columns:**
- `Drug_Name`: Compound name
- `PDB_Structure`: Structure ID (6VCB, 6XOX, 7E14, 7S15)
- `Glide_XP_Score`: Docking score
- `Glide_Emodel`: Emodel score
- `Rank`: Structure-specific rank (1 = best)

---

### 6. MM-GBSA Rescoring Results (CSV)

| File                                | Description                        | Size   |
|-------------------------------------|------------------------------------|--------|
| `mmgbsa_results_all_structures.csv` | N≈200 (top 50 per structure)       | 85 KB  |

**Columns:**
- `Drug_Name`: Compound name
- `PDB_Structure`: Structure ID
- `MM-GBSA_dG_Bind`: Binding free energy (kcal/mol)
- `MM-GBSA_dG_Bind_Coulomb`: Electrostatic contribution
- `MM-GBSA_dG_Bind_vdW`: Van der Waals contribution
- `MM-GBSA_dG_Bind_Lipo`: Lipophilic contribution
- `MM-GBSA_dG_Bind_Solv_GB`: Solvation penalty (GBSA)
- `Rank_MM-GBSA`: MM-GBSA rank (1 = best)
- `Z_score`: Normalized Z-score (structure-specific)

---

### 7. QikProp ADME Predictions (CSV)

| File                          | Description                        | Size   |
|-------------------------------|------------------------------------|--------|
| `qikprop_predictions_all.csv` | N=2,118 (all screened drugs)       | 520 KB |

**Columns:**
- `Drug_Name`: Compound name
- `Molecular_Weight`: MW (Da)
- `QPlogP`: Octanol/water partition coefficient
- `QPlogS`: Aqueous solubility (log S)
- `PSA`: Polar surface area (Å²)
- `HB_Donors`: H-bond donor count
- `HB_Acceptors`: H-bond acceptor count
- `Rotatable_Bonds`: Rotatable bond count
- `Percent_Oral_Absorption`: Predicted % oral absorption
- `Lipinski_Violations`: Rule-of-5 violation count
- `QED`: Quantitative Estimate of Drug-likeness (0-1)

---

### 8. Prime MM-GBSA Input Files

| File                                | Description                        | Size  |
|-------------------------------------|------------------------------------|-------|
| `prime_mmgbsa_input_6VCB.in`        | Prime MM-GBSA settings (6VCB)     | 1 KB  |
| `prime_mmgbsa_input_6XOX.in`        | Prime MM-GBSA settings (6XOX)     | 1 KB  |
| `prime_mmgbsa_input_7E14.in`        | Prime MM-GBSA settings (7E14)     | 1 KB  |
| `prime_mmgbsa_input_7S15.in`        | Prime MM-GBSA settings (7S15)     | 1 KB  |

**Key Settings:**
- Solvation model: VSGB (Variable-dielectric Generalized Born)
- Minimization: Local (pose optimization)
- Force field: OPLS4

---

## 🔄 Reproducibility

To reproduce the results:

1. **Download structures from PDB:**
   ```bash
   wget https://files.rcsb.org/download/6VCB.pdb
   wget https://files.rcsb.org/download/6XOX.pdb
   wget https://files.rcsb.org/download/7E14.pdb
   wget https://files.rcsb.org/download/7S15.pdb
   ```

2. **Prepare structures using Schrödinger:**
   - Use Protein Preparation Wizard (Maestro GUI)
   - Or run: `prepwizard -pH 7.4 -PROPKA <input.pdb> <output_prepared.pdb>`

3. **Generate docking grids:**
   - Use Receptor Grid Generation (Maestro GUI)
   - Grid centers from Table 1 (manuscript)

4. **Run Glide XP docking:**
   ```bash
   glide -JOBNAME <job_name> glide_xp_input_6VCB.in
   ```

5. **Run Prime MM-GBSA rescoring:**
   ```bash
   prime_mmgbsa -job_type REAL_MIN prime_mmgbsa_input_6VCB.in
   ```

6. **Run QikProp predictions:**
   ```bash
   qikprop -WAIT <ligand.sdf>
   ```

---

## 📊 File Size Summary

**Total Zenodo Deposit Size:** ~2.5 GB

| Category                  | File Count | Total Size |
|---------------------------|------------|------------|
| Prepared PDB structures   | 4          | 9.0 MB     |
| Docking grids             | 4          | 186 MB     |
| Docking input files       | 4          | 8 KB       |
| Top-ranked poses          | 10         | 1.0 MB     |
| Complete results (CSV)    | 3          | 1.8 MB     |
| MM-GBSA input files       | 4          | 4 KB       |
| **Supplementary (Zenodo)**| **29**     | **~2.5 GB**|

---

## 📜 License

**Data License:** CC BY 4.0 (Creative Commons Attribution 4.0 International)

**Citation Required:** See main README.md for citation format

---

## 📧 Contact

For data access issues or questions:
- **Email:** olaniyiolaniru@gmail.com
- **Zenodo Support:** support@zenodo.org

---

**Last Updated:** February 14, 2026


## Pre-GitHub supplementary data archive

A submission-ready, non-proprietary data package is provided as `Supplementary_Data_PreGitHub_v4_RSOS.zip` (prepared receptor PDBs, ligand library SDF, docked poses SDF/PDB, optional Glide grid archives, and PyMOL scripts).
