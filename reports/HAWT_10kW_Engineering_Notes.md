# HAWT 10 kW Wind Turbine - Engineering Design & Calculation Notes

**Document Identifier:** `HAWT-10kW-ENG-REV-01`  
**Target CAD Application:** Siemens NX / Siemens Designcenter (NX Student Edition 2606)  
**Author:** AI Mechanical Design Engineer & NX Automation Agent  
**Date:** 2026-10-01  
**Project Folder:** `C:\NaveenCADAgent`  

---

## 1. Design Requirements & System Specifications

| Parameter | Specification Target | Recommended Design Value | Status / Engineering Notes |
| :--- | :--- | :--- | :--- |
| **Rated Electrical Power ($P_{elec}$)** | $10\text{ kW}$ | $10.0\text{ kW}$ rated net ($11.2\text{ kW}$ gross calc.) | Meets requirement with ~12% electrical and thermal margin |
| **Rotor Diameter ($D$)** | $\sim 9.0\text{ m}$ | $9.0\text{ m}$ ($9,000\text{ mm}$) | Adopted |
| **Rotor Radius ($R$)** | $\sim 4.5\text{ m}$ | $4.5\text{ m}$ ($4,500\text{ mm}$) | Adopted |
| **Blade Count ($B$)** | 3 | 3 | Adopted (optimum small-wind aerodynamic balance and visual appeal) |
| **Hub Height ($H_{hub}$)** | $\sim 15.0\text{ m}$ | $15.0\text{ m}$ ($15,000\text{ mm}$) | Adopted |
| **Configuration** | Upwind, Horizontal Axis | Upwind, 3-bladed horizontal axis | Avoids tower-shadow blade fatigue typical of downwind machines |
| **Drivetrain Architecture** | Permanent Magnet Generator | Direct-Drive (PMG) conceptual arrangement | Eliminates high-speed gearbox maintenance, noise, and oil leak risks |
| **Rotor Speed Control** | Variable Speed / Pitch / Stall | Variable-speed torque control + aerodynamic pitch/stall | Optimum $C_p$ tracking across $3 - 9.5\text{ m/s}$ |

---

## 2. Operating & Environmental Assumptions

1. **Air Density ($\rho$):** $\rho = 1.225\text{ kg/m}^3$ (Standard Sea-Level Atmosphere: $T = 15^\circ\text{C} = 288.15\text{ K}$, $P = 101.325\text{ kPa}$).
2. **Cut-in Wind Speed ($V_{in}$):** $3.0\text{ m/s}$ ($\approx 10.8\text{ km/h}$). Below this speed, aerodynamic torque is insufficient to overcome bearing friction and generate useful power.
3. **Rated Wind Speed ($V_{rated}$):** $9.5\text{ m/s}$ ($\approx 34.2\text{ km/h}$). Standard IEC 61400-2 Class II/III small wind turbine rating point.
4. **Cut-out Wind Speed ($V_{cout}$):** $25.0\text{ m/s}$ ($\approx 90\text{ km/h}$). Active furling or blade aerodynamic pitch to feather triggers safe shutdown.
5. **Survival Wind Speed ($V_{50}$):** $50.0\text{ m/s}$ ($\approx 180\text{ km/h}$). 50-year extreme 3-second gust per IEC 61400-2 Class II.
6. **Aerodynamic Power Coefficient ($C_p$):** $C_{p,est} = 0.38$ at design Tip-Speed Ratio $\lambda = 7.0$ (Betz theoretical limit is $0.593$).
7. **Drivetrain & Electrical Efficiency:**
   - Permanent Magnet Generator: $\eta_{gen} = 0.92$ ($92\%$)
   - Mechanical bearings, windage, and seal losses: $\eta_{mech} = 0.96$ ($96\%$)
   - Total System Drivetrain Efficiency: $\eta_{tot} = 0.92 \times 0.96 = 0.8832$ ($88.3\%$).

---

## 3. Step-by-Step Engineering Sizing Calculations

### 3.1 Swept Area ($A$)
$$A = \pi \cdot R^2 = \pi \cdot (4.5\text{ m})^2 = 63.617\text{ m}^2$$

### 3.2 Total Kinetic Wind Power at Rated Speed ($P_{wind}$)
$$P_{wind} = \frac{1}{2} \cdot \rho \cdot A \cdot V_{rated}^3 = \frac{1}{2} \cdot (1.225) \cdot (63.617) \cdot (9.5)^3 = 33,408.2\text{ W} \approx 33.41\text{ kW}$$

### 3.3 Extracted Aerodynamic Power ($P_{aero}$)
$$P_{aero} = C_p \cdot P_{wind} = 0.38 \cdot 33,408.2\text{ W} = 12,695.1\text{ W} \approx 12.70\text{ kW}$$

### 3.4 Net Electrical Output Power ($P_{elec}$)
$$P_{elec} = \eta_{tot} \cdot P_{aero} = 0.8832 \cdot 12,695.1\text{ W} = 11,212.3\text{ W} \approx 11.21\text{ kW}$$
*Conclusion:* Exceeds the $10.0\text{ kW}$ threshold by $12.1\%$, providing realistic margin for grid inverter conversion losses, cable resistance, and minor aerodynamic fouling.

### 3.5 Rotor Kinematics (Tip Speed, Angular Velocity, RPM)
With design Tip-Speed Ratio $\lambda = 7.0$:
$$v_{tip} = \lambda \cdot V_{rated} = 7.0 \cdot 9.5\text{ m/s} = 66.50\text{ m/s}$$
$$\omega = \frac{v_{tip}}{R} = \frac{66.50\text{ m/s}}{4.5\text{ m}} = 14.778\text{ rad/s}$$
$$N = \frac{60 \cdot \omega}{2\pi} = \frac{60 \cdot 14.778}{2\pi} = 141.12\text{ RPM} \approx 141\text{ RPM}$$

### 3.6 Rotor Aerodynamic Torque ($Q$)
Rated operating aerodynamic torque:
$$Q_{rated} = \frac{P_{aero}}{\omega} = \frac{12,695.1\text{ W}}{14.778\text{ rad/s}} = 859.1\text{ N}\cdot\text{m}$$
Applying IEC 61400-2 gust dynamic factor ($K_{gust} = 1.5$):
$$Q_{design} = 1.5 \cdot 859.1\text{ N}\cdot\text{m} = 1,288.6\text{ N}\cdot\text{m} \approx 1.29\text{ kN}\cdot\text{m}$$

### 3.7 Rotor Aerodynamic Thrust ($T$)
Using 1D axial momentum theory with thrust coefficient $C_T \approx 0.80$ at peak $C_p$:
$$T_{rated} = \frac{1}{2} \cdot \rho \cdot A \cdot C_T \cdot V_{rated}^2 = \frac{1}{2} \cdot (1.225) \cdot (63.617) \cdot (0.80) \cdot (9.5)^2 = 2,813.3\text{ N} \approx 2.81\text{ kN}$$
Extreme survival thrust at $V_{50} = 50.0\text{ m/s}$ (blades parked/feathered with drag coefficient $C_{D,parked} \approx 0.15$):
$$T_{survival} = \frac{1}{2} \cdot \rho \cdot A \cdot C_{D,parked} \cdot V_{50}^2 = \frac{1}{2} \cdot (1.225) \cdot (63.617) \cdot (0.15) \cdot (50.0)^2 = 14,612.1\text{ N} \approx 14.61\text{ kN}$$

---

## 4. Subsystem Sizing & Structural Plausibility Checks

### 4.1 Main Rotor Shaft Diameter Sizing
- **Material:** 42CrMo4+QT / AISI 4140 alloy steel ($S_y = 650\text{ MPa}$, $S_{ut} = 900\text{ MPa}$).
- **Allowable Shear Stress:** $\tau_{allow} = \min(0.30 \cdot S_y, 0.18 \cdot S_{ut}) = 162\text{ MPa}$.
- Reduced by $25\%$ for keyway and shoulder stress concentration: $\tau_{allow,eff} = 121.5\text{ MPa}$.
- **Overhung Rotor Loads at Front Bearing Seat:**
  - Estimated rotor mass: Hub ($60\text{ kg}$) + 3 Blades ($3 \times 30\text{ kg} = 90\text{ kg}$) = $150\text{ kg}$.
  - Overhang distance: $L_{oh} = 250\text{ mm} = 0.25\text{ m}$.
  - Rotor weight: $W_{rotor} = 150 \times 9.81 = 1,471.5\text{ N}$.
  - Overhung bending moment: $M_b = W_{rotor} \cdot L_{oh} + T_{rated} \cdot 0.05\text{ m} = (1471.5 \times 0.25) + (2813.3 \times 0.05) = 508.5\text{ N}\cdot\text{m}$.
  - Design bending moment with fatigue/gust amplification ($K_b = 1.75$, $M_{extra} = 500\text{ N}\cdot\text{m}$ for gyroscopic precession): $M_{b,des} \approx 1,765\text{ N}\cdot\text{m}$.
- **ASME Combined Equivalent Torque:**
  $$T_e = \sqrt{(K_b \cdot M_{b,des})^2 + (K_t \cdot Q_{rated})^2} = \sqrt{(1.75 \times 1765)^2 + (1.25 \times 859.1)^2} = 3,269\text{ N}\cdot\text{m}$$
- **Minimum Theoretical Shaft Diameter:**
  $$d_{shaft,min} = \left( \frac{16 \cdot T_e}{\pi \cdot \tau_{allow,eff}} \right)^{1/3} = \left( \frac{16 \times 3269}{\pi \times 121.5 \times 10^6} \right)^{1/3} = 0.0516\text{ m} = 51.6\text{ mm}$$
- **Recommended CAD Dimension:** Standard ISO bearing journal diameter **$d_{bearing} = 75.0\text{ mm}$** (fits standard heavy-duty spherical roller bearing 22215 / 6215).
  - *Engineering Safety Margin:* Yields a fatigue factor of safety $FS > 3.0$ and restricts shaft angular deflection to $< 0.05^\circ$, ensuring long bearing roller life.

### 4.2 Blade Root Loading (Single Blade)
- **Flapwise Bending Moment ($M_{flap}$):**
  - Aerodynamic thrust per blade: $T_b = T_{rated} / 3 = 2,813.3 / 3 = 937.8\text{ N}$.
  - Center of aerodynamic pressure: $\bar{r} \approx 0.65 \cdot R = 2.925\text{ m}$.
  - Moment arm from blade root flange ($r_{root} = 0.30\text{ m}$): $L_{arm} = 2.925 - 0.30 = 2.625\text{ m}$.
  $$M_{flap,root} = 937.8\text{ N} \cdot 2.625\text{ m} = 2,461.6\text{ N}\cdot\text{m} \approx 2.46\text{ kN}\cdot\text{m}$$
- **Edgewise Bending Moment ($M_{edge}$):**
  - Blade mass $m_b = 30\text{ kg}$, center of gravity at $1.50\text{ m}$ from root:
  $$M_{edge,root} = (30\text{ kg} \cdot 9.81\text{ m/s}^2) \cdot 1.50\text{ m} = 441.5\text{ N}\cdot\text{m}$$
- **Centrifugal Axial Tension ($F_{cf}$):**
  - Center of mass from rotation axis $r_{cg} \approx 1.80\text{ m}$:
  $$F_{cf} = m_b \cdot r_{cg} \cdot \omega^2 = 30 \cdot 1.80 \cdot (14.778)^2 = 11,792.7\text{ N} \approx 11.79\text{ kN}$$
- **Root Circular Flange Sizing:**
  - Diameter: $D_{root} = 160\text{ mm}$.
  - Bolt Circle PCD $= 130\text{ mm}$ with 8x M14 Grade 10.9 high-tensile studs.
  - Tensile stress per stud under combined flapwise bending and centrifugal tension is $< 180\text{ MPa}$, well below the proof strength ($830\text{ MPa}$).

### 4.3 Tower Preliminary Loading & Base Reactions
- **Tower Geometry:** Truncated cone tubular steel shell.
  - Height: $H = 15.0\text{ m}$.
  - Base Outer Diameter: $D_{base} = 800\text{ mm}$, wall thickness $t = 8\text{ mm}$.
  - Top Outer Diameter: $D_{top} = 450\text{ mm}$, wall thickness $t = 8\text{ mm}$.
  - Total mass: $\approx 1,250\text{ kg}$ (Tower) + $500\text{ kg}$ (Rotor + Nacelle + Drivetrain) = $1,750\text{ kg}$.
- **Base Reactions under Extreme Survival Wind ($50\text{ m/s}$):**
  - Rotor survival thrust: $T_{survival} = 14.61\text{ kN}$ at $H = 15.0\text{ m}$.
  - Tower aerodynamic drag ($C_D = 0.70$, $D_{avg} = 0.625\text{ m}$): $F_{drag,tower} = 10.05\text{ kN}$ acting at $H/2 = 7.5\text{ m}$.
  - Overturning Bending Moment:
    $$M_{overturning,surv} = (14.61\text{ kN} \cdot 15.0\text{ m}) + (10.05\text{ kN} \cdot 7.5\text{ m}) = 219.15 + 75.38 = 294.5\text{ kN}\cdot\text{m}$$
  - Base Shear Force:
    $$V_{base,surv} = 14.61 + 10.05 = 24.66\text{ kN}$$
  - Vertical Compressive Gravity Reaction:
    $$F_{vertical} = 1,750\text{ kg} \cdot 9.81\text{ m/s}^2 = 17.17\text{ kN}$$
- **Tower Base Bending Stress:**
  - Section Modulus of hollow cylinder ($D_o = 800\text{ mm}, t = 8\text{ mm}$):
    $$Z_{base} = \frac{\pi}{4 \cdot D_o} \cdot (D_o^4 - D_i^4) \approx \frac{\pi}{4} \cdot D_o^2 \cdot t = \frac{\pi}{4} \cdot (0.800)^2 \cdot (0.008) = 0.00402\text{ m}^3$$
  - Maximum Bending Stress:
    $$\sigma_{bending} = \frac{M_{overturning,surv}}{Z_{base}} = \frac{294.5 \times 10^3\text{ N}\cdot\text{m}}{0.00402\text{ m}^3} = 73.2\text{ MPa}$$
  - Since $S_y = 355\text{ MPa}$ for S355 steel, the maximum stress is under $21\%$ of yield, providing high resistance against shell buckling and low-cycle fatigue.

### 4.4 Foundation Preliminary Sizing
- **Configuration:** Square shallow reinforced concrete gravity footing (C25/30).
- **Dimensions:** Width $B = 3.6\text{ m} \times 3.6\text{ m}$, depth $h = 0.8\text{ m}$, buried under $0.4\text{ m}$ soil overburden.
- **Stabilizing Weight:**
  - Concrete footing weight: $W_{conc} = (3.6 \times 3.6 \times 0.8) \times 2,400 \times 9.81 = 244.3\text{ kN}$.
  - Soil overburden weight: $W_{soil} = (3.6 \times 3.6 \times 0.4) \times 1,800 \times 9.81 = 91.5\text{ kN}$.
  - Turbine dead weight: $W_{turb} = 17.2\text{ kN}$.
  - Total vertical stabilizing load: $W_{tot} = 353.0\text{ kN}$.
- **Overturning Factor of Safety ($FS_{ot}$):**
  $$M_{stabilizing} = W_{tot} \cdot \frac{B}{2} = 353.0\text{ kN} \cdot 1.80\text{ m} = 635.4\text{ kN}\cdot\text{m}$$
  $$FS_{ot,survival} = \frac{635.4\text{ kN}\cdot\text{m}}{294.5\text{ kN}\cdot\text{m}} = 2.16 \ge 1.5\text{ (PASS)}$$
  $$FS_{ot,rated} = \frac{635.4}{42.2} = 15.06 \gg 2.0\text{ (PASS)}$$

---

## 5. Blade Aerodynamic Geometry Definition

### 5.1 Airfoil Selection: NACA 4412
- Thickness ratio: $12\%$ chord.
- Maximum camber: $4\%$ located at $40\%$ chord.
- Proven aerodynamic lift-to-drag ratio ($C_L / C_D > 75$ at $\alpha = 5^\circ - 7^\circ$), gentle stall progression, and structural depth for internal composite shear webs.

### 5.2 Radial Station Distribution & Loft Parameters

| Station No. | Radial Position $r$ ($\text{mm}$) | Fraction $r/R$ | Profile / Airfoil Type | Chord $c$ ($\text{mm}$) | Twist Angle $\beta$ ($^\circ$) | Local Thickness $t$ ($\text{mm}$) | Engineering Function |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **0** | $300$ | $0.067$ | Circular Root | $160$ ($\varnothing$) | $+16.0$ | $160$ | Hub pitch bearing / flange bolt circle interface |
| **1** | $675$ | $0.150$ | Thick Elliptical Transition | $380$ | $+14.5$ | $106$ ($t/c \approx 28\%$) | Aerodynamic transition, high flapwise bending section modulus |
| **2** | $1,125$ | $0.250$ | NACA 4412 | $420$ | $+12.0$ | $50.4$ | Maximum chord station (Schmitz optimum profile) |
| **3** | $1,575$ | $0.350$ | NACA 4412 | $370$ | $+9.5$ | $44.4$ | High torque generation zone |
| **4** | $2,250$ | $0.500$ | NACA 4412 | $310$ | $+6.5$ | $37.2$ | Mid-span aerodynamic workhorse |
| **5** | $2,925$ | $0.650$ | NACA 4412 | $250$ | $+4.0$ | $30.0$ | High relative velocity, optimized lift/drag |
| **6** | $3,600$ | $0.800$ | NACA 4412 | $195$ | $+2.0$ | $23.4$ | Outer span high dynamic pressure |
| **7** | $4,050$ | $0.900$ | NACA 4412 | $160$ | $+0.8$ | $19.2$ | Taper region for vortex mitigation |
| **8** | $4,410$ | $0.980$ | NACA 4412 | $130$ | $0.0$ | $15.6$ | Aerodynamic tip station |
| **9** | $4,500$ | $1.000$ | Rounded Tip Cap | $60$ | $0.0$ | $7.2$ | Smooth aerodynamic tip closure |

---

## 6. Manufacturing, Assembly & Maintenance Considerations

1. **Blade Fabrication:**
   - Two-piece female mold vacuum-assisted resin infusion (VARI) using epoxy resin and E-glass biaxial/UD fabrics.
   - Root section incorporates metallic insert bushings or T-bolt pockets directly infused into the root layup.
   - Upper and lower aerodynamic shells bonded along the leading and trailing edges with structural epoxy adhesive paste, with internal shear web bonded simultaneously.

2. **Hub Machining & Casting:**
   - One-piece sand-cast ductile iron (EN-GJS-400-18-LT).
   - Single CNC setup for turning the rear shaft mounting spigot and boring the central hollow core.
   - 4-axis or 5-axis CNC milling for the three blade mounting faces and bolt hole patterns spaced at $120.00^\circ$.

3. **Shaft & Bearing Assembly:**
   - 42CrMo4 forged round bar, rough turned, quenched and tempered, finish ground at bearing journals to ISO m5 / k5 fits.
   - Front bearing pressed against locating shaft shoulder with induction heating; locked axially with a precision locknut (KM series) and lock washer.
   - Rear bearing floating axially in housing bore to accommodate thermal expansion.

4. **Nacelle & Tower Erection Sequence:**
   - Pre-drilled anchor bolt cage cast into concrete foundation block with template ring.
   - Tower segments raised via mobile crane, preloaded with calibrated torque wrenches to EN 14399 standard.
   - Nacelle bedplate with pre-installed yaw bearing and generator lifted and bolted to tower top flange.
   - Pre-assembled rotor (Hub + 3 Blades + Spinner) lifted in a single lift and mated to the main shaft flange via high-tensile preloaded bolts.

---

## 7. Limitations & Disclaimer

This preliminary design document, engineering calculations, and associated NX CAD models are produced strictly for **engineering concept, prototype feasibility study, and parametric CAD automation**. They do **NOT** constitute certified construction drawings or type certification under IEC 61400-2 / DNV-GL. Full finite element analysis (FEA), multi-body dynamic simulation (AeroDyn / FAST / OpenFAST), boundary layer wind tunnel validation, and extreme turbulence fatigue testing must be performed prior to physical manufacturing.

---

## 8. Revision 2 CAD Model Enhancements (FEA Interface & Base Fasteners)

Following visual audit and engineering interface review in Siemens NX, the CAD model has been updated with the following structural refinements:

### 8.1 Tower Base Anchor Fastener Assemblies (Hex Nuts & Modeled M24 Metric Threads)
- **Problem Resolved:** The original base model featured bare cylindrical studs protruding through the base flange without clamping hardware or screw threads.
- **Implementation:** Added 16 complete M24 anchor assemblies on Pitch Circle Diameter (PCD) $920\text{ mm}$:
  - **ISO 7089 M24 Hardened Washers:** $\varnothing 44\text{ mm} \text{ OD} \times 4\text{ mm}\text{ thick}$, resting flush on top of the $35\text{ mm}$ base flange ($Z = 185.0\text{ mm}$ to $189.0\text{ mm}$).
  - **ISO 4032 / DIN 934 M24 Hexagonal Nuts:** Width across flats $s = 36.0\text{ mm}$, height $m = 19.0\text{ mm}$, circumscribed diameter $41.57\text{ mm}$ ($Z = 189.0\text{ mm}$ to $208.0\text{ mm}$).
  - **3D Modeled ISO 68-1 / ISO 261 M24 Metric Threads:**
    - Standard coarse pitch: $P = 3.0\text{ mm}$.
    - Major diameter: $D_{maj} = 24.0\text{ mm}$ (radius $12.0\text{ mm}$).
    - Minor diameter: $D_{min} = 20.3\text{ mm}$ (radius $10.15\text{ mm}$).
    - Thread profile: 60° triangular metric V-thread form with 12 distinct annular thread pitches spanning the exposed stud ($Z = 208.0\text{ mm}$ to $244.0\text{ mm}$).
    - Tip finishing: 45° chamfered lead-in cone ($Z = 244.0\text{ mm}$ to $247.0\text{ mm}$) per standard bolt manufacturing specifications.

### 8.2 Foundation Clearance & Rogue Cone Elimination
- **Problem Resolved:** A stray red/orange conical body appeared at ground level due to an unshifted workplane offset in the spinner nose cone.
- **Root Cause & Correction:** The nose cone loft was previously generated on the global origin $XZ$ plane ($Z = 0$). All hub components (`hub_barrel`, `hub_nose`, `hub_nose_tip`, `hub_bosses`) have now been rigorously constructed on positive-normal planes centered at hub elevation $Z = H_{hub} = 15,630.0\text{ mm}$. The ground envelope ($Z = -800\text{ mm}$ to $Z = +245\text{ mm}$) now contains exclusively the concrete foundation block, pedestal, tower base flange, and anchor bolt assemblies.

### 8.3 Rotor Hub & Blade Root FEA Interface
- **Problem Resolved:** The nacelle fairing previously extended to $Y = +850\text{ mm}$, swallowing the hub barrel and causing the blades to appear protruding directly from the nacelle canopy.
- **Nacelle-Hub Separation:**
  - Nacelle front bulkhead terminates cleanly at $Y = +280.0\text{ mm}$ with a $\varnothing 280\text{ mm}$ shaft collar opening.
  - Rotating hub backplate begins at $Y = +320.0\text{ mm}$, establishing a realistic $40\text{ mm}$ running clearance gap.
  - Hub central barrel spans $Y = +320.0\text{ mm}$ to $+560.0\text{ mm}$ ($\varnothing 560\text{ mm}$ OD).
  - Aerodynamic spinner dome smoothly lofts from $Y = +560.0\text{ mm}$ to $+980.0\text{ mm}$ with a rounded nose tip reaching $Y = +1040.0\text{ mm}$.
- **FEA-Feasible Blade Attachment:**
  - Rotor pitch plane is situated at $Y_{rotor} = +520.0\text{ mm}$.
  - Three heavy ductile iron radial mounting bosses extend outward from the hub core in the $XZ$ plane ($120^\circ$ spacing).
  - Each boss terminates at radius $r = 340.0\text{ mm}$ with a machined $\varnothing 250\text{ mm} \times 25\text{ mm}$ pitch bearing mounting flange and 12x M16 pitch bolt studs on PCD $210\text{ mm}$.
  - Each blade begins at $r = 340.0\text{ mm}$ with a matching circular root flange ($\varnothing 230\text{ mm} \times 25\text{ mm}$ thick) that sits flush against the hub boss face.
  - The blade root transitions through a structural cylindrical sleeve ($\varnothing 175\text{ mm}$) to the high-thickness NACA 4412 airfoil section at $r = 720.0\text{ mm}$.
  - This establishes a continuous, planar circular contact face at $r = 340.0\text{ mm}$, allowing direct application of bonded surface-to-surface contact, coincident meshing, or bolt pretension elements in Siemens NX Simcenter 3D / Nastran FEA.

---

## 9. Revision 3 CAD Enhancements (True Helical Drive Threads & Rotatable Blades)

### 9.1 True 3D Continuous Helical Drive Screw Threads
- **Engineering Justification:** In high-stiffness structural anchoring, anchor bolts transmit intense cyclic tensile and prying fatigue loads into the foundation grout and embedment cage. True 3D continuous helical teeth accurately capture the lead angle ($\lambda = \arctan(P / (\pi \cdot d_2)) \approx 2.4^\circ$), stress distribution along engaged thread teeth, and accurate cross-sectional stiffness for high-fidelity 3D FEA meshing.
- **Parametric Generation:**
  - Standard: ISO 68-1 / ISO 261 M24 x 3.0 coarse metric thread.
  - Path: Continuous 3D spatial helix generated via `Wire.makeHelix(pitch=3.0, height=36.0, radius=12.0)`.
  - Cutter Profile: 60° triangular metric cutter swept along the helix using Frenet framing (`isFrenet=True`), cutting clean spiral helical grooves into the solid steel cylindrical blank.
  - Tip Lead-in: 45° conical lead-in chamfer for standard bolt engagement.
  - Geometry: 12 full continuous 3D helical spiral turns across all 16 anchor studs ($Z = 208.0\text{ mm}$ to $244.0\text{ mm}$).

### 9.2 Rotatable Blades & Kinematic Degrees of Freedom for FEA
- **FEA Operational Requirements:**
  - **Blade Pitch Degree of Freedom ($\theta_{pitch}$):** Wind turbine blades must rotate about their longitudinal radial pitch axis (from $0^\circ$ operational fine pitch to $90^\circ$ full aerodynamic feathering for extreme storm survival). In NX Simcenter 3D, this allows evaluating flapwise and edgewise stress states across the entire pitch envelope.
  - **Rotor Azimuth Degree of Freedom ($\theta_{azimuth}$):** Wind turbine loads vary drastically with rotor clock angle due to wind shear (power law gradient) and the tower shadow effect when a blade passes vertically in front of the tower at $\theta_{azimuth} = 180^\circ$ (6 o'clock).
- **CAD & Assembly Implementation:**
  - **Independent Component Tree:** All 3 blades are saved as independent, unmerged top-level solids in the STEP assembly: `Blade_01_NACA4412_Rotatable`, `Blade_02_NACA4412_Rotatable`, and `Blade_03_NACA4412_Rotatable`.
  - **Precision Revolute Journal:** Each blade root incorporates a concentric cylindrical sleeve ($\varnothing 175\text{ mm}$) and circular flange ($\varnothing 230\text{ mm}$) sharing a common revolute axis with the hub's radial boss ($\varnothing 250\text{ mm}$).
  - **NX Constraint Mating:** In Siemens NX Assembly, users can apply a **Touch / Align $\rightarrow$ Concentric** constraint and freely rotate the blades to any pitch angle or use NX **Move Component $\rightarrow$ Rotate** interactively.
  - **Script Parameters:** Exposed `ROTOR_AZIMUTH_DEG` and `BLADE_PITCH_DEG` at the top of the CAD journal for automated batch multi-angle FEA exports.


