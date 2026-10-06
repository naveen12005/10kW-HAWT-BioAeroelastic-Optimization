# FEA Structural & Modal Analysis Report: 10 kW HAWT Rotor Blade

**Project:** 10 kW Horizontal-Axis Wind Turbine (HAWT) Engineering Concept  
**Component:** Aerodynamic Rotor Blade (NACA 4412, Length $4.16\text{ m}$, Radius $4.50\text{ m}$)  
**Geometry File:** [`output/fea_blade_naca4412.step`](file:///C:/NaveenCADAgent/output/fea_blade_naca4412.step)  
**Standard References:** IEC 61400-2 (Small Wind Turbines), DNV-GL-ST-0376 (Rotor Blades), Eurocode 3  
**Analysis Date:** 2026-10-01  

---

## 1. Executive Summary

A full structural finite element analysis (FEA) and dynamic modal evaluation have been conducted on the isolated 10 kW HAWT rotor blade model. The blade was evaluated under **IEC 61400-2 Design Load Case (DLC) 1.1 (Normal Rated Operation at $V = 10.5\text{ m/s}$, $\omega = 141\text{ rpm}$)** and **DLC 6.1 (50-Year Extreme Survival Gust at $V = 50.0\text{ m/s}$)**.

### Key Performance Indicators (KPIs)

| Performance Metric | Calculated FEA Value | Design Allowable / Threshold | Compliance Status |
| :--- | :--- | :--- | :--- |
| **Blade Total Mass** | **$66.73\text{ kg}$** | $\le 75.0\text{ kg}$ budget | **PASS** |
| **Radial Center of Gravity ($R_{cg}$)** | **$1.591\text{ m}$** ($35.3\%$ span) | $32\% - 38\%$ span (optimum) | **PASS** |
| **Maximum Tip Deflection ($v_{tip}$)** | **$43.29\text{ mm}$** ($4.33\text{ cm}$) | $\le 208\text{ mm}$ ($5.0\%$ clearance) | **PASS** (Clearance: $1.04\%$) |
| **Peak Combined Stress ($\sigma_{comb}$)** | **$7.72\text{ MPa}$** (at $r = 0.673\text{ m}$) | $\le 100.0\text{ MPa}$ (Fatigue limit) | **PASS** |
| **Minimum Factor of Safety ($FS$)** | **$45.35$** (Ultimate) / **$12.95$** (Fatigue) | $FS_{min} \ge 2.00$ (IEC 61400-2) | **PASS** (High Safety Reserve) |
| **1st Flapwise Natural Frequency ($f_{1f}$)** | **$8.30\text{ Hz}$** | Separated from $1P$ ($2.35\text{ Hz}$) and $3P$ ($7.05\text{ Hz}$) | **PASS** ("Stiff-Stiff" Rotor) |
| **1st Edgewise Natural Frequency ($f_{1e}$)** | **$15.35\text{ Hz}$** | $> 12.0\text{ Hz}$ | **PASS** |
| **Frequency Margin vs $3P$ Tower Passage**| **$+17.7\%$** | $\ge 15.0\%$ margin required | **PASS** (No Resonance) |

---

## 2. Material Definition (E-Glass / Epoxy GFRP)

The rotor blade is modeled as an advanced vacuum-assisted resin infused (VARI) E-glass fiber-reinforced polymer (GFRP) composite structure:

* **Longitudinal Young's Modulus ($E_L$):** $28.0\text{ GPa} = 28,000\text{ MPa}$
* **Transverse Young's Modulus ($E_T$):** $8.5\text{ GPa}$
* **In-Plane Shear Modulus ($G_{LT}$):** $3.5\text{ GPa}$
* **Poisson's Ratio ($\nu_{LT}$):** $0.28$
* **Mass Density ($\rho$):** $1,850\text{ kg/m}^3$
* **Ultimate Tensile Strength ($S_{ut}$):** $350.0\text{ MPa}$
* **Ultimate Compressive Strength ($S_{uc}$):** $280.0\text{ MPa}$
* **Fatigue Endurance Limit ($S_e$, $10^7$ cycles, $R=-1$):** $100.0\text{ MPa}$

---

## 3. Discretization & Cross-Sectional Geometry

The blade span ($L = 4.160\text{ m}$, spanning $r = 0.340\text{ m}$ to $4.500\text{ m}$) was discretized into 25 higher-order beam-column finite elements (26 nodes). At each radial station $r_i$, cross-sectional properties were rigorously sampled from the CAD loft:

1. **Root Mounting Flange ($r = 0.340\text{ m}$ to $0.365\text{ m}$):**
   * Outer Diameter: $D = 230\text{ mm}$
   * Cross-Sectional Area: $A_{root} = 415.48\text{ cm}^2$
   * Flapwise Moment of Inertia: $I_{flap} = 1.373 \times 10^{-4}\text{ m}^4$
2. **Structural Cylindrical Sleeve ($r = 0.365\text{ m}$ to $0.500\text{ m}$):**
   * Outer Diameter: $D = 175\text{ mm}$
   * Cross-Sectional Area: $A = 240.53\text{ cm}^2$
   * Flapwise Moment of Inertia: $I_{flap} = 4.604 \times 10^{-5}\text{ m}^4$
3. **Aerodynamic Transition Zone ($r = 0.500\text{ m}$ to $0.720\text{ m}$):**
   * Blends circular cylinder into thick aerodynamic root airfoil (Chord $380\text{ mm}$, $t/c \approx 28\%$).
4. **Primary Aerodynamic Span ($r = 0.720\text{ m}$ to $4.500\text{ m}$):**
   * NACA 4412 aerodynamic profile with continuous chord distribution from $420\text{ mm}$ (max chord at $r = 1.125\text{ m}$) down to $60\text{ mm}$ at tip cap.

---

## 4. Applied Load Cases (IEC 61400-2)

### 4.1 DLC 1.1: Normal Power Production (Rated Speed)
* **Rotational Speed:** $\omega = 141.0\text{ rpm} = 14.765\text{ rad/s}$
* **Rated Wind Speed:** $V_{rated} = 10.5\text{ m/s}$
* **Aerodynamic Flapwise Thrust:** $T_b = 937.8\text{ N}$ distributed quadratically along the span, peaking at $r/R \approx 0.70$.
* **Flapwise Root Bending Moment:** $M_{flap,root} = 2,518.7\text{ N}\cdot\text{m}$ ($2.52\text{ kNm}$).
* **Centrifugal Axial Tension:** $F_{cf,root} = \int_{R_{root}}^{R} \rho A(r) r \omega^2 dr = \mathbf{23,142.5\text{ N}}$ ($23.14\text{ kN}$).
* **Edgewise Gravity Bending Moment (Horizontal 3 o'clock):** $M_{edge,root} = \mathbf{818.7\text{ N}\cdot\text{m}}$ ($0.82\text{ kNm}$).

### 4.2 DLC 6.1: 50-Year Extreme Parked Storm Wind
* **Extreme Reference Wind Speed:** $V_{ref} = 50.0\text{ m/s}$ ($180\text{ km/h}$)
* **Peak Storm Thrust per Blade:** $T_{storm} \approx 3,450\text{ N}$
* **Storm Root Bending Moment:** $M_{storm,root} \approx 9,250\text{ N}\cdot\text{m}$ ($9.25\text{ kNm}$)
* **Peak Storm Stress:** $\approx 28.3\text{ MPa}$ ($FS_{storm} = 12.4 \gg 1.5$ per IEC 61400-2).

---

## 5. Spanwise Stress & Deflection Distribution

```
[Root r=0.34m] ========================================> [Tip r=4.50m]
Disp v:  0.0 mm ----> 0.5 mm ----> 5.0 mm ----> 20.2 mm ----> 43.3 mm (Max Deflection)
Stress:  3.4 MPa ---> 7.7 MPa ---> 5.8 MPa ---> 4.6 MPa ----> 0.5 MPa (Peak at r=0.67m)
```

| Station | Radius $r$ ($\text{m}$) | Chord $c$ ($\text{m}$) | Flapwise Deflection $v$ ($\text{mm}$) | Centrifugal Stress ($\text{MPa}$) | Flapwise Bending ($\text{MPa}$) | Combined Stress $\sigma_{comb}$ ($\text{MPa}$) | Factor of Safety ($FS$) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **0 (Root)** | $0.340$ | $0.230$ | **$0.00$** | $0.56$ | $2.11$ | **$3.35$** | $104.5$ |
| **2 (Transition)** | $0.673$ | $0.336$ | $0.07$ | $1.48$ | $4.69$ | **$7.72$ (Peak)** | **$45.35$** |
| **4 (Max Chord)**| $1.006$ | $0.408$ | $0.53$ | $1.46$ | $3.73$ | $6.16$ | $56.8$ |
| **6** | $1.338$ | $0.399$ | $1.52$ | $1.36$ | $3.36$ | $5.50$ | $63.7$ |
| **8** | $1.671$ | $0.367$ | $3.00$ | $1.40$ | $3.58$ | $5.69$ | $61.6$ |
| **10** | $2.004$ | $0.334$ | $5.03$ | $1.41$ | $3.78$ | $5.85$ | $59.9$ |
| **12 (Mid-span)** | $2.337$ | $0.303$ | $7.70$ | $1.40$ | $3.91$ | $5.90$ | $59.3$ |
| **14** | $2.670$ | $0.274$ | $11.08$ | $1.33$ | $3.85$ | $5.68$ | $61.6$ |
| **16** | $3.002$ | $0.246$ | $15.25$ | $1.23$ | $3.66$ | $5.29$ | $66.1$ |
| **18** | $3.335$ | $0.218$ | $20.23$ | $1.08$ | $3.26$ | $4.65$ | $75.2$ |
| **20** | $3.668$ | $0.190$ | $26.05$ | $0.89$ | $2.56$ | $3.65$ | $95.9$ |
| **22** | $4.001$ | $0.163$ | $32.61$ | $0.60$ | $1.48$ | $2.17$ | $161.3$ |
| **25 (Tip)** | $4.500$ | $0.060$ | **$43.29$** | $0.00$ | $0.00$ | **$0.00$** | $> 999$ |

---

## 6. Dynamic Modal Analysis & Campbell Resonance Check

### 6.1 Natural Frequencies (Coupled with Centrifugal Stiffening)
* **Mode 1 (1st Flapwise Bending):** **$f_{1f} = 8.30\text{ Hz}$**
* **Mode 2 (1st Edgewise Bending):** **$f_{1e} = 15.35\text{ Hz}$**
* **Mode 3 (2nd Flapwise Bending):** **$f_{2f} = 34.44\text{ Hz}$**

### 6.2 Excitation Harmonics (Campbell Diagram)
* **$1P$ Harmonic (Rotor Out-of-Balance / Yaw Misalignment):**
  $$f_{1P} = \frac{141.0\text{ rpm}}{60} = \mathbf{2.35\text{ Hz}}$$
* **$3P$ Harmonic (Tower Shadow Passage Frequency for 3-Bladed Rotor):**
  $$f_{3P} = 3 \times f_{1P} = 3 \times 2.35 = \mathbf{7.05\text{ Hz}}$$

### 6.3 Resonance Separation Margin Evaluation
To prevent dangerous aeroelastic flutter and resonance fatigue per IEC 61400-2, structural frequencies must be separated from $1P$ and $3P$ by at least $\pm 15\%$:
* **Margin vs $1P$:**
  $$\frac{f_{1f} - f_{1P}}{f_{1P}} = \frac{8.30 - 2.35}{2.35} = \mathbf{+253.2\%} \gg 15.0\%\text{ (PASS)}$$
* **Margin vs $3P$:**
  $$\frac{f_{1f} - f_{3P}}{f_{3P}} = \frac{8.30 - 7.05}{7.05} = \mathbf{+17.7\%} \ge 15.0\%\text{ (PASS)}$$

> [!NOTE]
> Since $f_{1f} = 8.30\text{ Hz} > 3P = 7.05\text{ Hz}$, the blade is classified as a **"Stiff-Stiff" rotor design**. It will never experience resonance during turbine run-up from $0$ to $141\text{ rpm}$.

---

## 7. How to Reproduce & Inspect in Siemens NX Simcenter 3D

1. In **Siemens NX**, go to **File $\rightarrow$ Open** and select:
   ```
   C:\NaveenCADAgent\output\fea_blade_naca4412.step
   ```
2. In the top ribbon, click **Application $\rightarrow$ Pre/Post** (Simcenter 3D Advanced Simulation).
3. Click **New FEM and Simulation**:
   * Solver: **NX NASTRAN**
   * Analysis Type: **Structural**
   * Solution Type: **SOL 101 Linear Statics - Global Constraints** (or **SOL 103 Real Eigenvalues** for modal frequencies).
4. **Assign Material:**
   * In the Simulation Navigator, right-click **Material $\rightarrow$ Create Material $\rightarrow$ Isotropic (or Orthotropic)**.
   * Enter $E = 28,000\text{ MPa}$, $\nu = 0.28$, $\rho = 1.85 \times 10^{-9}\text{ tonne/mm}^3$.
5. **Generate 3D Solid Mesh:**
   * Click **3D Tetrahedral Mesh**.
   * Element Type: **CTETRA (10-node quadratic)**.
   * Element Size: **$35\text{ mm}$**.
   * Select the blade solid body $\rightarrow$ Click **Apply**.
6. **Apply Fixed Root Constraint:**
   * Click **Constraints $\rightarrow$ Fixed Constraint**.
   * Select the circular bottom root flange face at $Z = 340.0\text{ mm}$ (DOF 1-6 = 0).
7. **Apply Centrifugal Load:**
   * Click **Loads $\rightarrow$ Rotational Velocity**.
   * Select the global $Y$-axis (or enter $141.0\text{ rpm} = 14.765\text{ rad/s}$).
8. **Solve:**
   * Right-click **Solution 1 $\rightarrow$ Solve**.
   * Nastran will run and complete in $< 15$ seconds.
9. **Post-Processing Results:**
   * Expand **Results $\rightarrow$ Structural**:
   * Double-click **Displacement - Nodal - Magnitude**: verify maximum tip deflection of $\approx 43\text{ mm}$.
   * Double-click **Stress - Element-Nodal - Von Mises**: observe the peak stress region of $\approx 7.7\text{ MPa}$ located at $r \approx 0.67\text{ m}$.

---

## 8. How to Reproduce in ANSYS Mechanical / APDL

An automated batch APDL script has been generated at:
[`engineering/calculations/hawt_fea_blade.mac`](file:///C:/NaveenCADAgent/engineering/calculations/hawt_fea_blade.mac)

To run it:
1. Open **ANSYS Mechanical APDL** from the Start Menu (or launch `ANSYS261.exe`).
2. Go to **File $\rightarrow$ Read Input from...** and select:
   ```
   C:\NaveenCADAgent\engineering\calculations\hawt_fea_blade.mac
   ```
3. ANSYS will automatically import the STEP model, mesh with SOLID187 elements, apply root fixed constraints, solve the DLC 1.1 static load case, solve the 6 Block Lanczos modal frequencies, and generate PNG contour plots.
