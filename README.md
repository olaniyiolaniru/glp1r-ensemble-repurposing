# GLP-1R Drug Repurposing - Complete Submission Package

## Overview
This repository contains all materials for the manuscript:

**"Computational Repurposing Screen Identifies Oral Drug Candidates for GLP-1 Receptor Modulation"**


## 📁 Repository Structure
│
├── Figures/                                     # All 8 main figures
│   ├── Figure1_Pocket_Equivalence.png
│   ├── Figure2_Reference_Benchmarking.png
│   ├── Figure3_Docking_Rescoring_Correlation.png
│   ├── Figure4_Outcome_Class_Separation.png
│   ├── Figure5_Cross_Structure_Robustness.png
│   ├── Figure6_Binding_Mode_Analysis.png
│   ├── Figure7_Structure_Activity.png
│   ├── Figure8_ChEMBL_Validation.png
│   
│
├── Supplementary_Tables/                        # All 12 supplementary tables
│   └── Supplementary_Tables_S1-S12.xlsx         # Excel workbook with 12 sheets
│
├── Python_Scripts/                              # Analysis & visualization code
│   ├── figure1_pocket_equivalence.py
│   ├── figure2_reference_benchmarking.py
│   ├── figure3_docking_rescoring_correlation.py
│   ├── figure4_outcome_class_separation.py
│   ├── figure5_cross_structure_robustness.py
│   ├── figure6_binding_mode_analysis.py
│   ├── figure7_structure_activity.py
│   ├── figure8_chembl_validation.py
│  
│
├── PyMOL_Scripts/                               # 3D structural visualization
│   ├── figure6_overlays.pml                     # Binding mode overlays
│   └── supplementary_pocket_alignment.pml       # Pocket conservation analysis
│
└── Data/                                         
    ├── README_data.md                       
    └── (PDB structures, docking poses, etc. - deposited on Zenodo)
```

---

## 🚀 Quick Start

### 1. Generate All Figures

**Requirements:**
- Python 3.8+
- Libraries: numpy, pandas, matplotlib, seaborn, scipy, openpyxl

**Installation:**
```bash
cd Python_Scripts/
pip install -r requirements.txt
```

**Run all figure scripts:**
```bash
python figure1_pocket_equivalence.py
python figure2_reference_benchmarking.py
python figure3_docking_rescoring_correlation.py
python figure4_outcome_class_separation.py
python figure5_cross_structure_robustness.py
python figure6_binding_mode_analysis.py
python figure7_structure_activity.py
python figure8_chembl_validation.py
```

Figures will be saved to `../Figures/` in both PNG (300 dpi) and TIFF (300 dpi) formats.

---

### 2. Generate Supplementary Tables

```bash
python generate_supplementary_tables.py
```

Creates `../Supplementary_Tables/Supplementary_Tables_S1-S12.xlsx` with 12 sheets:
- **S1**: Structure quality metrics (Ramachandran, clash scores)
- **S2**: Per-structure docking results (N=2,118 compounds)
- **S3**: MM-GBSA rescoring output (N≈50 per structure)
- **S4**: QikProp descriptor predictions
- **S5**: Consensus ranking (n_struct ≥ 3)
- **S6**: Exposure-plausible shortlist (n=10 drugs)
- **S7**: Interaction probe classification
- **S8**: Pose retention sensitivity analysis
- **S9**: Enrichment factors (EF₁%, EF₅%, EF₁₀%)
- **S10**: Active/decoy benchmark set
- **S11**: ChEMBL cross-reference data
- **S12**: Drug-drug interaction predictions

---

### 3. Generate 3D Structural Overlays (PyMOL)

**Requirements:**
- PyMOL 2.5+ (https://pymol.org)
- Prepared PDB structures and docked poses (see Data/ folder)

**Usage:**
```bash
cd PyMOL_Scripts/
pymol figure6_overlays.pml              # Binding mode overlays
pymol supplementary_pocket_alignment.pml # Pocket conservation
```

**Note:** Requires the following files in `../Data/`:
- `6VCB_prepared.pdb`, `6XOX_prepared.pdb`, `7E14_prepared.pdb`, `7S15_prepared.pdb`
- `eltrombopag_7S15_top_pose.sdf`
- `netarsudil_7E14_top_pose.sdf`
- `apixaban_6XOX_top_pose.sdf`

---

## 📊 Key Findings

### Top 10 Exposure-Plausible Drug Candidates

| Rank | Drug Name              | ChEMBL ID    | Primary Indication     | Mean ΔG (kcal/mol) | Oral Bioavailability (%) |
|------|------------------------|--------------|------------------------|--------------------|--------------------------|
| 1    | Eltrombopag            | CHEMBL461101 | Thrombocytopenia       | -76.2              | 52                       |
| 2    | Netarsudil             | CHEMBL4594250| Glaucoma               | -73.5              | 35                       |
| 3    | Apixaban               | CHEMBL231779 | Thromboembolism        | -72.1              | 50                       |
| 4    | Rivaroxaban            | CHEMBL198362 | Thromboembolism        | -70.8              | 80                       |
| 5    | Sacubitril             | CHEMBL4297299| Heart failure          | -69.5              | 60                       |
| 6    | Edoxaban               | CHEMBL1173055| Thromboembolism        | -68.2              | 62                       |
| 7    | Betrixaban             | CHEMBL3039474| Thromboembolism        | -67.8              | 34                       |
| 8    | Dabigatran etexilate   | CHEMBL1127   | Thromboembolism        | -66.5              | 3 (prodrug)              |
| 9    | Bempedoic acid         | CHEMBL3301571| Hypercholesterolemia   | -65.2              | 38                       |
| 10   | Ezetimibe              | CHEMBL1138   | Hypercholesterolemia   | -64.1              | 50                       |

### Reference-Ligand Benchmarking Performance

| PDB Structure | Reference Ligand  | RRP   | 95% CI        | EF₁₀% | Classification  |
|---------------|-------------------|-------|---------------|-------|-----------------|
| 7S15          | PF-06882961       | 1.00  | (0.93, 1.00)  | 9.60  | Excellent       |
| 7E14          | LY3502970         | 0.98  | (0.90, 1.00)  | 8.67  | Excellent       |
| 6XOX          | LY3502970         | 0.92  | (0.81, 0.98)  | 8.50  | Excellent       |
| 6VCB          | LSN3160440        | 0.60  | (0.45, 0.74)  | 0.00  | Moderate        |

---

## 🔬 Methodology Summary

### Ensemble Docking Protocol

1. **Structure Preparation:**
   - 4 GLP-1R cryo-EM structures (PDB: 6VCB, 6XOX, 7E14, 7S15)
   - Schrödinger Protein Preparation Wizard (pH 7.4, PROPKA)
   - Grid generation centred on orforglipron binding pocket

2. **Virtual Screening:**
   - Library: 2,118 approved drugs (e-Drug3D database)
   - Glide XP docking (Schrödinger Suite 2023-4)
   - Top 50 poses per structure advanced to rescoring

3. **MM-GBSA Rescoring:**
   - Prime MM-GBSA (VSGB solvation model)
   - Z-score normalisation for cross-structure consensus
   - ΔΔG framing relative to reference ligands

4. **ADME Filtering:**
   - QikProp 2D descriptor prediction
   - Filters: PSA ≤ 140 Å², oral absorption ≥ 80%, Lipinski compliant
   - Exposure-plausible if n_struct ≥ 3 and favorable ADME

5. **Validation:**
   - ChEMBL v34 experimental property validation
   - Reference-ligand benchmarking (RRP, enrichment factors)
   - Binding mode analysis (H-bonding, hydrophobic interactions)

---

## 📚 Citation

**If you use this code or data, please cite:**

```bibtex
@article{Olaniru2026GLP1R,
  title={Computational Repurposing Screen Identifies Oral Drug Candidates for GLP-1 Receptor Modulation},
  author={Olaniru, Olaniyi Victor and Jesulude, Peace Dorcas and Ajiboye, Clement Odunayo},
  journal={Royal Society Open Science},
  year={2026},
  note={Manuscript in review}
}
```

---

## 📦 Data Availability

### Zenodo Repository
All raw data, docking grids, and top-ranked poses are deposited at:
**DOI:** Pending (Zenodo will mint a DOI when archiving this GitHub release)

**Contents:**
- Glide docking grids (4 structures, .zip)
- Glide XP input files (.in)
- Prime MM-GBSA input files
- Top-ranked poses (SDF format)
- Complete docking/MM-GBSA tables (CSV)
- QikProp output (CSV)

### GitHub Repository
All analysis code is available at:
**URL: Repo: https://github.com/olaniyiolaniru/glp1r-ensemble-repurposing
Release (v1.0.3): https://github.com/olaniyiolaniru/glp1r-ensemble-repurposing/releases/tag/v1.0.3
Supplementary ZIP (direct download): https://github.com/olaniyiolaniru/glp1r-ensemble-repurposing/releases/download/v1.0.0/Supplementary_Data.zip
**

**License:** MIT

---

## 🛠️ Software Requirements

### Computational Chemistry
- **Schrödinger Suite 2023-4** (commercial license required)
  - Maestro (structure preparation)
  - Glide XP (docking)
  - Prime MM-GBSA (rescoring)
  - QikProp (ADME prediction)

### Analysis & Visualization
- **Python 3.8+** (free)
  - numpy, pandas, matplotlib, seaborn, scipy, openpyxl
- **PyMOL 2.5+** (open-source or educational license)
- **Microsoft Excel / LibreOffice Calc** (for supplementary tables)

---

## 👥 Authors

**Olaniyi Victor Olaniru** (Corresponding Author)
- Affiliation: Lead City University, Ibadan, Nigeria
- Email: olaniyiolaniru@gmail.com
- ORCID: https://orcid.org/0009-0008-9853-6335

**Peace Dorcas Jesulude**
- Affiliation: Lead City University, Ibadan, Nigeria
- Email: peacejesulude@gmail.com
- ORCID: https://orcid.org/0009-0005-9646-3564

**Clement Odunayo Ajiboye**
- Affiliation: University of Ibadan, Ibadan, Nigeria
- Email: co.ajiboye@ui.edu.ng
- ORCID: https://orcid.org/0000-0002-6205-8828

---

## 🔒 License

**Code:** MIT License (see LICENSE file)

**Data:** CC BY 4.0 (Creative Commons Attribution 4.0 International)

**Manuscript:** Copyright © 2026 The Royal Society. All rights reserved.

---

## 📞 Contact

For questions about the computational methods, code, or data:
- **Email:** olaniyiolaniru@gmail.com
- **Issues:** Submit via GitHub Issues (once repository is public)

---

## 🙏 Acknowledgments

- **Schrödinger Inc.** for academic software licenses
- **RCSB Protein Data Bank** for GLP-1R structural data
- **ChEMBL** (EMBL-EBI) for experimental validation data
- **e-Drug3D** curators (D. Douguet) for approved drug library
- **Royal Society Open Science** for open peer review process

---

## 📅 Version History

- **v1.0** (2026-02-14): Initial submission package
  - All 8 figures generated (300+ dpi TIFF/PNG)
  - All 12 supplementary tables (Excel workbook)
  - Complete Python analysis scripts
  - PyMOL visualisation scripts
  - README and documentation

---

**Last Updated:** February 14, 2026


## Pre-GitHub supplementary data archive

A submission-ready, non-proprietary data package is provided as `Supplementary_Data.zip` (prepared receptor PDBs, ligand library SDF, docked poses SDF/PDB, optional Glide grid archives, and PyMOL scripts).
