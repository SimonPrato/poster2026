# Equivalent Circuit Models of Near-Field Coupling between Electrically Small Antennas and TEM Cells

**Simon Prato** — Institute of Fundamentals and Theory in Electrical Engineering,
Graz University of Technology, Austria
Supervised by Prof. T. Bauernfeind

Conference paper for **POSTER 2026**, Prague, May 2026.

---

## Abstract

Bond wires in optical sensor ICs (e.g. VCSELs) form electrically small loops that
radiate unwanted EMI. Because the apertures required for light transmission prevent
full shielding, this work develops lumped-element equivalent circuit models (EQCs)
for the near-field coupling between electrically small antennas and TEM cells.

EQC parameters are extracted from FEM simulations (Ansys HFSS). Coupling behaviour
is validated against FEM across 1 MHz – 3 GHz, with agreement within ±2 %. The EQC
reveals that the electric dipole moment arises from capacitive coupling (via *C*_k) and
the magnetic dipole moment from inductive coupling between antenna and septum
inductances.

---

## Repository Structure

```
01_references/   Background literature (PDFs)
02_paper/        Conference paper — LaTeX source and compiled PDF
03_scripts/      Python scripts: EQC computation and result plotting
04_notes/        Working notes, planning docs, LaTeX draft sections
05_templates/    IEEE LaTeX and poster templates
06_spice/        LTspice schematic files for EQC circuit verification
```

---

## Key Results

- **Loop antenna**: both capacitive (*C*_k) and inductive (*M*) coupling paths active;
  *C*_A = 38.2 fF, *L*_A = 2.14 nH.
- **Monopole antenna**: predominantly capacitive coupling (*M* ≈ 0);
  *C*_A = 98.4 fF, *L*_A = 1.14 nH, *C*_k ≈ 1.68 pF.
- EQC simulations run orders of magnitude faster than the corresponding FEM models.

---

## References

1. IEC 61967-8: *Measurement of Radiated Emissions — IC Stripline Method*, 2023.
2. T. Ostermann & B. Deutschmann, "TEM-Cell and Surface Scan to Identify the
   Electromagnetic Emission of ICs," GLSVLSI 2003, pp. 76–79.
3. D. Kreindl et al., "A Simulation Workflow for Predicting IC Stripline Radiated
   Emissions of Bond Wire-Based Systems," EMC Compo 2024, pp. 69–73.
