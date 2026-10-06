# Engineering Standards Reference for HAWT 10 kW Wind Turbine

This document summarizes the recognized engineering standards, codes of practice, and design formulas applied in the preliminary engineering design and CAD modeling of the 10 kW Horizontal-Axis Wind Turbine.

---

## 1. Primary Wind Turbine Standards

### IEC 61400-2: Small Wind Turbines (Ed. 3)
- **Scope:** Applies to wind turbines with rotor swept area up to $200\text{ m}^2$ (our $9\text{ m}$ rotor has swept area $A = 63.62\text{ m}^2$, fully governed by IEC 61400-2).
- **Wind Turbine Class:** Class II / Class III assumed:
  - Reference annual average wind speed: $V_{ave} = 7.5 - 8.5\text{ m/s}$
  - Reference 50-year extreme 3-second gust: $V_{ref} = 50.0\text{ m/s}$ ($V_{e50} = 1.4 \times V_{ref} = 52.5\text{ m/s}$ simplified simplified to $50\text{ m/s}$)
  - Normal Turbulence Model (NTM): Turbulence intensity $I_{15} \approx 18\%$
- **Design Load Cases (DLCs):**
  - DLC 1.1 / 1.2: Normal power production ($V_{in} \le V \le V_{cout}$)
  - DLC 2.1: Power production with electrical grid disconnection / generator loss of load
  - DLC 5.1: Emergency shutdown
  - DLC 6.1 / 6.2: Parked / idling under 50-year extreme wind ($V_{50} = 50\text{ m/s}$)
- **Partial Safety Factors for Simplified Load Methodology (SLM):**
  - Aerodynamic load partial safety factor: $\gamma_f = 1.35$
  - Gravity / dead-weight load partial safety factor: $\gamma_f = 1.10$
  - Material partial safety factor for steel components: $\gamma_m = 1.15$
  - Material partial safety factor for FRP composite blade: $\gamma_m = 2.2 - 2.5$ (accounting for environmental degradation, moisture, temperature, and cyclic fatigue)

---

## 2. Structural & Mechanical Design Standards

### ASME B106.1M / ANSI / AGMA 6001-E08 (Shaft & Drivetrain Sizing)
- **Shaft Design Methodology:** Combined torsion and bending under dynamic cyclic loading.
- **Equivalent Torsional Moment Formula:**
  $$T_e = \sqrt{(K_b \cdot M_b)^2 + (K_t \cdot T)^2}$$
  - $K_b = 1.75$ (combined shock and fatigue bending factor for rotating shafts with moderate shock)
  - $K_t = 1.25$ (combined shock and fatigue torsion factor)
- **Allowable Shear Stress:**
  $$\tau_{allow} = \min(0.30 \cdot S_y, 0.18 \cdot S_{ut})$$
  Reduced by $25\%$ for stress concentration at keyways / shoulder fillets ($\tau_{allow,eff} = 0.75 \cdot \tau_{allow}$).

### ISO 281 & ISO 76 (Rolling Bearings)
- **Rating Life ($L_{10h}$):** Minimum required bearing operating life for small wind turbines: $L_{10h} \ge 100,000\text{ hours}$ (~11.4 years continuous operation).
- **Bearing Arrangement:**
  - Front bearing: Double-row spherical roller bearing (e.g. ISO 22215) or heavy-duty deep groove ball bearing located close to hub to react heavy radial overhang moment and axial thrust.
  - Rear bearing: Deep groove ball bearing / cylindrical roller bearing (e.g. ISO 6215 / NU 215) accommodating shaft thermal expansion.

### Eurocode 3 (EN 1993-1-1 / EN 1993-1-6) - Tower Shell & Steel Structures
- **Tubular Tower Design:**
  - Circumferential and longitudinal shell buckling resistance verified against EN 1993-1-6.
  - Maximum top deflection under rated operation limited to: $\delta_{top} \le H / 100 = 150\text{ mm}$.
  - First tower bending natural frequency ($f_0$) placed outside the 1P and 3P blade excitation bands ("soft-stiff" design):
    - 1P excitation band at rated RPM ($141.1\text{ RPM}$): $f_{1P} = 2.35\text{ Hz}$
    - 3P excitation band (blade passing frequency): $f_{3P} = 3 \times 2.35 = 7.05\text{ Hz}$
    - Target tower natural frequency: $f_0 \approx 1.2 - 1.8\text{ Hz}$ (well below 1P or between 1P and 3P).

### Eurocode 2 (EN 1992-1-1) - Concrete Foundation
- **Footing Design:** Reinforced concrete slab (C25/30 / C30/37).
- **Overturning Factor of Safety:**
  $$FS_{overturning} = \frac{M_{stabilizing}}{M_{overturning}} \ge 2.0\text{ (Rated)}, \quad \ge 1.5\text{ (Survival 50 m/s)}$$
- **Soil Bearing Pressure:**
  $$q_{max} \le q_{allowable} \approx 150 - 200\text{ kPa}$$
  No tension across more than 25% of the footing footprint under extreme loading.

---

## 3. Fastener Standards

### ISO 898-1 (Mechanical Properties of Fasteners)
- **Blade Root Studs / T-Bolts:** Metric Grade 10.9 ($S_y = 940\text{ MPa}$, $S_{ut} = 1040\text{ MPa}$)
- **Hub Flange Bolts:** Metric Grade 10.9 or 8.8 ($S_y = 640\text{ MPa}$, $S_{ut} = 830\text{ MPa}$)
- **Tower Flange Preloaded Bolts:** Metric Grade 10.9 (EN 14399 HV structural bolting assemblies)
- **Anchor Bolts (Foundation):** High-yield anchor rods (Grade 8.8 or ASTM A354 Grade BD).
