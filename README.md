POSTER 2026 — OVERVIEW
======================
Conference : CEFC 2026 (Computation of Electromagnetic Fields Conference)
Authors    : Simon Prato, Dominik Kreindl, Thomas Bauernfeind
             Institute of Fundamentals and Theory in Electrical Engineering,
             Graz University of Technology, Graz, Austria

PAPER TITLE
-----------
"Capacitive and Inductive Near-Field Coupling of Electrically Small
 Antennas in TEM Cells via Equivalent Circuit Models"

ONE-LINE SUMMARY
----------------
Lumped-element (equivalent circuit) models are developed for the electric
(capacitive) and magnetic (inductive) near-field coupling of a monopole and
a loop antenna inside a TEM cell, validated against FEM results in Ansys HFSS.

═══════════════════════════════════════════════════════
FOLDER STRUCTURE
═══════════════════════════════════════════════════════

  plan.txt                ← MAIN PLANNING DOCUMENT — start here
  README.md               ← this file

  01_references/          ← Background reading
  │   Documentation_MasterThesis_Prato.pdf
  │       Simon's master thesis (100 pp.): full theoretical framework,
  │       dipole theory, TEM cell modes, FEM, EQC models, shielding.
  │       This is the primary source for the paper content.
  └── ACES2024_Kreindl_Official.pdf
          Kreindl et al. (ACES 2024): paper whose introduction is closely
          followed for the CEFC 2026 paper intro.

  02_paper/               ← Conference paper (LaTeX source + output)
  │   CEFC2026_Bauernfeind.tex          ← main LaTeX source (edit this)
  │   CEFC2026_Prato_Kreindl_Bauernfeind.pdf ← compiled output (current draft)
  │   conference_101719.tex/.pdf        ← older/alternate draft
  │   figures/                          ← all images used in the paper
  │       VCSEL.png                     motivation: VCSEL device
  │       test_loop.png                 gapped loop antenna geometry
  │       antenna.png / antenna_1.png   additional antenna structures
  │       dipole_moments_loop_antenna.png  dipole moment schematic
  │       gapped_loop_moments.png / _corr.png  me & mm vs. freq (FEM)
  │       s12_meas.png / s12_meas_1.png IC stripline cross-section / setup
  │       fig1.png                      (TBD)
  └── build/                            ← LaTeX build artifacts + IEEEtran class
          IEEEtran.cls / IEEEtran_HOWTO.pdf, .aux/.bbl/.blg/.log files

  03_scripts/             ← Python scripts to compute & plot results
  │   eqc-cap-antenna/    monopole EQC: compute dipole moments from circuit
  │   eqc-ind-antenna/    loop antenna EQC: compute dipole moments from circuit
  │   evaluate-moments/   evaluate FEM dipole moments over frequency
  │   field-calc-expr/    field calculation expressions (.clc)
  └── generic-plotting/   general-purpose plotting from FEM data

  04_notes/               ← Working notes & ideas
  │   eqc.txt             LaTeX-formatted EQC sections (monopole + loop):
  │                       circuit derivations, component values, equations
  │   notes.txt           brief one-liner note on VCSEL motivation
  └── Ideen_fuer_extendedAbstract.pdf  brainstorming doc for paper structure

  05_templates/           ← Document templates
      latextemplate.zip   IEEE LaTeX template (base)
      poster2026template.docx  Word template for poster layout

═══════════════════════════════════════════════════════
PAPER STRUCTURE (two pages)
═══════════════════════════════════════════════════════

  1. Introduction
     - VCSEL shielding impossible → need EQC-based coupling analysis
     - TEM cell as FEM surrogate for IC stripline
     - Electrically small → lumped-element representation valid

  2. TEM Cell Measurement
     - Dipole moment extraction from two-port TEM cell measurements
     - |me| = |U1+U2|·h/ZW,  |mm| = |U1-U2|·h·Z0/ZW

  3. Equivalent Circuit + Results
     - Monopole: capacitive coupling (C_k), C_A=98.4 fF, L_A=1.14 nH
     - Loop: both capacitive (C_k) and inductive (M) coupling,
             C_A=38.2 fF, L_A=2.14 nH
     - Phase difference as indicator of me/mm balance
     - FEM vs. EQC comparison for both antennas

═══════════════════════════════════════════════════════
KEY REFERENCES
═══════════════════════════════════════════════════════
  - D. Kreindl et al., ACES 2024 (intro model, IC stripline workflow)
  - T. Ostermann & B. Deutschmann, GLSVLSI 2003 (TEM cell IC measurement)
  - IEC 61967-8 (IC stripline standard)
  - L.J. Chu, J. Appl. Phys. 1948 (electrically small antenna theory)
  - C.A. Balanis, Antenna Theory, 1997 (loop antenna EQC)
