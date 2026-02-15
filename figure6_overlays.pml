# PyMOL script to reproduce Figure 6 overlays (RSOS submission package)
# Run from within PyMOL: File > Run... scripts/figure6_overlays_RSOS.pml

# Load prepared receptors (protein-only) from this package
load ../Data/6XOX_prepared.pdb, ref_6XOX
load ../Data/7S15_prepared.pdb, rec_7S15
load ../Data/7E14_prepared.pdb, rec_7E14

# Align ensemble receptors to the reference (6XOX)
align rec_7S15, ref_6XOX
align rec_7E14, ref_6XOX

# Load top poses (ligands only; SDF exported from Glide poseviewer)
load ../Data/eltrombopag_7S15_top_pose.sdf, eltrombopag
load ../Data/netarsudil_7E14_top_pose.sdf, netarsudil
load ../Data/apixaban_6XOX_top_pose.sdf, apixaban

# Put all ligands into the same pocket frame (6XOX)
align eltrombopag, ref_6XOX
align netarsudil, ref_6XOX
align apixaban, ref_6XOX

# Display
hide everything
show cartoon, ref_6XOX
color gray70, ref_6XOX
set cartoon_transparency, 0.3, ref_6XOX

show sticks, eltrombopag
show sticks, netarsudil
show sticks, apixaban

# Optional: highlight key pocket residues (edit selection if needed)
select pocket_resi, (ref_6XOX and resi 190+227+231+235+260+261+264+265)
show sticks, pocket_resi
color yellow, pocket_resi

# Aesthetics
set stick_radius, 0.18
set ray_opaque_background, off
set antialias, 2
zoom (eltrombopag or netarsudil or apixaban), 8
