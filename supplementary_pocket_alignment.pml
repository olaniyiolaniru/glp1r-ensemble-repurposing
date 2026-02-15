# PyMOL script to reproduce supplementary pocket alignment overlay (RSOS submission package)
# Run from within PyMOL: File > Run... scripts/supplementary_pocket_alignment_RSOS.pml

load ../Data/6XOX_prepared.pdb, rec_6XOX
load ../Data/7E14_prepared.pdb, rec_7E14
load ../Data/7S15_prepared.pdb, rec_7S15
load ../Data/6VCB_prepared.pdb, rec_6VCB

# Align all to 6XOX
align rec_7E14, rec_6XOX
align rec_7S15, rec_6XOX
align rec_6VCB, rec_6XOX

hide everything
show cartoon, rec_6XOX or rec_7E14 or rec_7S15 or rec_6VCB
set cartoon_transparency, 0.6
set antialias, 2

# Optional pocket residue selection in the 6XOX frame
select pocket_resi, (rec_6XOX and resi 190+227+231+235+260+261+264+265)
show sticks, pocket_resi
color yellow, pocket_resi

zoom rec_6XOX, 10
