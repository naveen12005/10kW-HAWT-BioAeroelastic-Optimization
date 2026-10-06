# Material Specifications for HAWT 10 kW Wind Turbine

This document defines the preliminary engineering material selections, physical and mechanical properties, and design justifications for each major subsystem of the 10 kW Horizontal-Axis Wind Turbine.

---

## 1. Summary Material Selection Table

| Subsystem / Component | Material Designation | Material Class | Density $\rho$ ($\text{kg/m}^3$) | Yield Strength $S_y$ ($\text{MPa}$) | Tensile Strength $S_{ut}$ ($\text{MPa}$) | Young's Modulus $E$ ($\text{GPa}$) | Poisson's Ratio $\nu$ | Primary Design Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Blades (Shell & Spar)** | E-Glass / Epoxy UD & Triaxial Laminate | Glass-Fiber Reinforced Polymer (GFRP) | 1,850 | ~250 (Tensile) / ~200 (Comp.) | ~400 (Longitudinal) | 28 - 32 | 0.28 | High fatigue strength-to-weight ratio, corrosion resistance, automated vacuum infusion |
| **Blade Root Insert Ring** | Structural Steel S355J2 | Structural Steel (EN 10025-2) | 7,850 | 355 | 510 | 210 | 0.30 | High bearing strength for root stud bushings / T-bolt connections |
| **Rotor Hub** | EN-GJS-400-18-LT (GGG-40.3) | Ductile Cast Iron (SGI) | 7,100 | 250 | 400 | 169 | 0.28 | Outstanding low-temperature impact toughness ($-20^\circ\text{C}$ Charpy $\ge 12\text{ J}$), vibration damping, casting complex 3-way geometry |
| **Main Rotor Shaft** | 42CrMo4+QT (AISI 4140) | Alloy Steel (Quenched & Tempered) | 7,850 | 650 | 900 | 210 | 0.30 | High fatigue limit, deep hardenability, resistance to combined torsion, bending, and shock loads |
| **Bearing Housing** | EN-GJL-250 (GG-25) | Grey Cast Iron | 7,200 | 165 (Proof) | 250 | 110 | 0.26 | High compressive strength, excellent vibration absorption, dimensional stability |
| **Tower Tubular Shell** | Structural Steel S355JR / S355NL | Structural Steel (EN 10025) | 7,850 | 355 | 490 - 630 | 210 | 0.30 | High weldability, high yield strength for slender shell buckling resistance, standard rolled plate availability |
| **Tower Flanges** | S355NL / Forged Steel | Forged Structural Steel | 7,850 | 355 | 520 | 210 | 0.30 | High through-thickness ductility, flat machined mating faces for preloaded bolted joints |
| **Bedplate / Nacelle Frame** | Structural Steel S275JR / S355JR | Welded Structural Steel Plate / Tube | 7,850 | 275 - 355 | 430 - 510 | 210 | 0.30 | High rigidity for driveline alignment, welded construction |
| **Nacelle Cover & Spinner** | Chopped Strand Mat (CSM) / Vinyl Ester | Fiber Composite | 1,500 | ~70 | ~120 | 10 | 0.32 | Lightweight aerodynamic fairing, weather protection, non-structural shell |
| **Foundation Block** | Concrete C25/30 (EN 206) + Rebar B500B | Reinforced Concrete | 2,400 | 25 (Char. Cyl. $f_{ck}$) | 30 (Char. Cube) | 31 | 0.20 | Massive gravity stabilization against overturning, high compressive strength |
| **Anchor Bolts** | High-Tensile Grade 8.8 / 10.9 Steel | Fastener Alloy Steel | 7,850 | 640 / 940 | 800 / 1040 | 210 | 0.30 | Fatigue-resistant preloaded anchoring in concrete foundation |

---

## 2. Component Design Considerations

### 2.1 Rotor Blade (GFRP Composite)
- **Aero Shell:** Bi-axial ($\pm 45^\circ$) E-glass fabric with epoxy resin for torsional stiffness and aerodynamic contour definition.
- **Main Spar Cap:** Unidirectional ($0^\circ$) E-glass roving / fabric positioned along the quarter-chord region (top and bottom) to absorb flapwise aerodynamic bending moments.
- **Shear Webs:** Glass/epoxy sandwich with PVC/PET foam core to resist cross-sectional shear and prevent local wall buckling.
- **Root Bushings:** Metallic threaded inserts (M14) potted in reinforced circular root ring to mate with hub blade mounting pads.

### 2.2 Rotor Hub (Cast Ductile Iron)
- Ductile iron EN-GJS-400-18-LT provides the optimum balance of machinability, impact toughness in freezing winds, and casting economics for a 3-way symmetrical junction.
- Wall thickness: $25 - 35\text{ mm}$ around blade roots, blending with generous fillets ($R = 20 - 40\text{ mm}$) into the central tubular barrel to avoid notch stress concentrations under cyclic blade flapwise bending.

### 2.3 Main Shaft (42CrMo4 / AISI 4140)
- Quenched and tempered alloy steel provides an endurance limit $S_e' \approx 0.5 \cdot S_{ut} \approx 450\text{ MPa}$.
- With surface finish factor $k_a \approx 0.85$, size factor $k_b \approx 0.75$, reliability factor $k_c \approx 0.897$ ($90\%$ reliability), and temperature factor $k_d = 1.0$:
  $$S_e = 450 \cdot (0.85 \cdot 0.75 \cdot 0.897) \approx 257\text{ MPa}$$
- At $d = 75\text{ mm}$, the maximum cyclic reversed bending stress under rated operating conditions is under $55\text{ MPa}$, yielding an infinite-life fatigue safety margin:
  $$FS_{fatigue} = \frac{257}{55} \approx 4.67 \gg 2.0$$

### 2.4 Tower Shell (S355JR)
- High-strength structural steel sheet ($t = 8\text{ mm}$) rolled into truncated conical sections and circumferentially welded.
- Internal zinc primer and external polyurethane high-durability marine paint (C5-M exposure rating) for 20+ year atmospheric corrosion resistance.
