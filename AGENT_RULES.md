# Naveen CAD Agent - Core Operating Rules

These rules govern all CAD design prompts and engineering workflows:

1. **Dimensional Integrity & Standards Consultation:**
   - Never silently change user-specified dimensions.
   - If a standard engineering value is superior or required (e.g., preferred diameters, DIN 6885 / IS 2048 keys, standard fits/tolerances, standard tool radii/fillets), explicitly recommend it, explain the engineering rationale, and ask the user for confirmation before applying changes.

2. **Engineering Priority Hierarchy:**
   - **Safety > Standards > Function > Manufacturability > Optimization > Cost > User Preference.**

3. **Explicit Assumptions & Analytical Rigor:**
   - Explicitly state all engineering assumptions (e.g., applied forces, torques, material properties, yield/ultimate strengths, factor of safety, operating RPM, service conditions).
   - Show all underlying formulas, derivations, and step-by-step calculations.
   - Never claim a design is "safe" without verified engineering stress/deflection analysis.

4. **Design Generation & Output Standards:**
   - For every design, write a parametric CadQuery script to `designs/<name>.py`.
   - Export the 3D geometry in STEP format to `output/<name>.step`.
   - Execute the design script via `run_design.ps1 <name>`.

5. **NX Boundary & Response Deliverables (Option 3 - Manual Import):**
   - **Strict NX Boundary:** This rule strictly forbids interacting with Siemens NX. Never launch NX, attach to NX, or send any keystrokes, clicks, or GUI automation to NX. The user manually imports the generated STEP files into Siemens NX via `File -> Import -> STEP`.
   - **Engineering Rules Retained:** This rule does NOT replace any engineering requirements. For every design response, the agent must provide:
     1. Stated assumptions (loads, service environment, RPM, material, safety factors).
     2. Step-by-step calculations and sizing derivations.
     3. Recommended deviations/standards (if applicable), asking the user before applying them.
     4. Physical and geometric telemetry:
        - Full path to the generated STEP file
        - Volume ($\text{mm}^3$)
        - Bounding Box ($X \times Y \times Z$ in $\text{mm}$)
        - Mass ($\text{g}$ or $\text{kg}$)
   - Once these engineering deliverables and telemetry are reported, stop.
