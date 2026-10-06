import os
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

os.makedirs("reports/portfolio_figures", exist_ok=True)
print("Generating High-Resolution Portfolio Figures for Rotor Blade FEA...")

# --- DATA FROM FEA SOLVER ---
radii = [
    0.340, 0.506, 0.673, 0.839, 1.006, 1.172, 1.338, 1.505, 1.671, 1.838,
    2.004, 2.170, 2.337, 2.503, 2.670, 2.836, 3.002, 3.169, 3.335, 3.502,
    3.668, 3.834, 4.001, 4.167, 4.334, 4.500
]
chord = [
    0.230, 0.175, 0.336, 0.392, 0.408, 0.418, 0.399, 0.381, 0.367, 0.350,
    0.334, 0.318, 0.303, 0.288, 0.274, 0.260, 0.246, 0.232, 0.218, 0.204,
    0.190, 0.176, 0.163, 0.149, 0.136, 0.060
]
disp_v = [
    0.00, 0.01, 0.07, 0.23, 0.53, 0.96, 1.52, 2.20, 3.00, 3.94,
    5.03, 6.28, 7.70, 9.30, 11.08, 13.06, 15.25, 17.63, 20.23, 23.03,
    26.05, 29.25, 32.61, 36.08, 39.68, 43.29
]
sigma_comb = [
    3.35, 2.80, 7.72, 6.85, 6.16, 5.80, 5.50, 5.60, 5.69, 5.78,
    5.85, 5.88, 5.90, 5.82, 5.68, 5.50, 5.29, 5.00, 4.65, 4.20,
    3.65, 2.95, 2.17, 1.35, 0.47, 0.00
]
sigma_flap = [
    2.11, 1.60, 4.69, 4.10, 3.73, 3.50, 3.36, 3.45, 3.58, 3.69,
    3.78, 3.85, 3.91, 3.90, 3.85, 3.78, 3.66, 3.50, 3.26, 2.95,
    2.56, 2.05, 1.48, 0.88, 0.29, 0.00
]
sigma_tensile = [
    0.56, 0.70, 1.48, 1.47, 1.46, 1.42, 1.36, 1.38, 1.40, 1.41,
    1.41, 1.41, 1.40, 1.37, 1.33, 1.28, 1.23, 1.16, 1.08, 0.99,
    0.89, 0.76, 0.60, 0.40, 0.18, 0.00
]

# ------------------------------------------------------------------------------
# FIGURE 1: SPANWISE STRESS & DEFLECTION DISTRIBUTION
# ------------------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), dpi=300, sharex=True)

# Deflection plot
ax1.plot(radii, disp_v, color='#0066cc', lw=2.5, marker='o', markersize=4, label='Flapwise Deflection $v(r)$')
ax1.axhline(43.29, color='red', linestyle='--', lw=1.2, label='Max Tip Deflection ($43.3$ mm)')
ax1.axhline(208.0, color='darkred', linestyle=':', lw=1.5, label='IEC Clearance Limit (5% span = $208$ mm)')
ax1.set_ylabel('Deflection [mm]', fontsize=11, fontweight='bold')
ax1.set_title('10 kW HAWT Rotor Blade: Structural FEA Results (IEC 61400-2 DLC 1.1)', fontsize=13, fontweight='bold', pad=12)
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.legend(loc='upper left', frameon=True)
ax1.set_ylim(-2, 60)

# Annotation for tip deflection
ax1.annotate(f'Tip Deflection = 43.3 mm\n(1.04% of Span)',
             xy=(4.5, 43.29), xytext=(3.5, 20),
             arrowprops=dict(facecolor='#0066cc', shrink=0.08, width=1.5, headwidth=6),
             fontsize=9, fontweight='bold', bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.9))

# Stress plot
ax2.plot(radii, sigma_comb, color='#cc0000', lw=2.5, marker='s', markersize=4, label='Peak Combined Stress $\\sigma_{comb}$')
ax2.plot(radii, sigma_flap, color='#ff6600', lw=1.8, linestyle='-.', label='Flapwise Bending Stress $\\sigma_{flap}$')
ax2.plot(radii, sigma_tensile, color='#009933', lw=1.8, linestyle=':', label='Centrifugal Tensile Stress $\\sigma_{t}$')
ax2.axhline(100.0, color='purple', linestyle='--', lw=1.5, label='Fatigue Endurance Limit ($S_e = 100$ MPa)')
ax2.set_xlabel('Rotor Radial Position $r$ [m]', fontsize=11, fontweight='bold')
ax2.set_ylabel('Stress [MPa]', fontsize=11, fontweight='bold')
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.legend(loc='upper right', frameon=True)
ax2.set_ylim(0, 15)

# Annotation for peak stress
ax2.annotate('Peak Stress = 7.72 MPa\n(Transition Zone r = 0.67 m)\nFOS = 45.4 (Yield) / 12.9 (Fatigue)',
             xy=(0.673, 7.72), xytext=(1.2, 10.5),
             arrowprops=dict(facecolor='#cc0000', shrink=0.08, width=1.5, headwidth=6),
             fontsize=9, fontweight='bold', bbox=dict(boxstyle='round,pad=0.4', facecolor='#fff2f2', edgecolor='#cc0000', alpha=0.9))

plt.tight_layout()
fig1_path = "reports/portfolio_figures/fig1_blade_fea_stress_deflection.png"
fig.savefig(fig1_path)
plt.close(fig)
print(f"[1/2] Figure 1 saved to: {fig1_path}")

# ------------------------------------------------------------------------------
# FIGURE 2: CAMPBELL DIAGRAM (RESONANCE EVALUATION)
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 7), dpi=300)

rpm_range = [0, 30, 60, 90, 120, 141, 160, 180]
f_1P = [rpm / 60.0 for rpm in rpm_range]
f_3P = [3.0 * (rpm / 60.0) for rpm in rpm_range]

# Blade natural frequencies with centrifugal stiffening: f(rpm) = sqrt(f0^2 + S * (rpm/60)^2)
f1_flap_0 = 8.10
f1_flap = [math.sqrt(f1_flap_0**2 + 1.2 * (rpm / 60.0)**2) for rpm in rpm_range]

f1_edge_0 = 15.20
f1_edge = [math.sqrt(f1_edge_0**2 + 0.8 * (rpm / 60.0)**2) for rpm in rpm_range]

f2_flap_0 = 34.00
f2_flap = [math.sqrt(f2_flap_0**2 + 3.0 * (rpm / 60.0)**2) for rpm in rpm_range]

# Excitation lines
ax.plot(rpm_range, f_1P, color='#333333', lw=2.0, linestyle='--', label='1P Excitation Harmonic (1 rev/sec)')
ax.plot(rpm_range, f_3P, color='#ff9900', lw=2.5, linestyle='-', label='3P Blade Passage Harmonic (3 blades)')

# 15% Exclusion Band around 3P
f_3P_upper = [1.15 * f for f in f_3P]
f_3P_lower = [0.85 * f for f in f_3P]
ax.fill_between(rpm_range, f_3P_lower, f_3P_upper, color='#ff9900', alpha=0.15, label='±15% Resonance Exclusion Band')

# Structural Natural Frequencies
ax.plot(rpm_range, f1_flap, color='#0066cc', lw=2.8, marker='o', markersize=5, label='1st Flapwise Bending ($f_{1f} = 8.30$ Hz at rated)')
ax.plot(rpm_range, f1_edge, color='#009933', lw=2.2, marker='s', markersize=5, label='1st Edgewise Bending ($f_{1e} = 15.35$ Hz)')
ax.plot(rpm_range, f2_flap, color='#9900cc', lw=2.0, marker='^', markersize=5, label='2nd Flapwise Bending ($f_{2f} = 34.44$ Hz)')

# Rated speed line
ax.axvline(141.0, color='red', linestyle=':', lw=1.8, label='Rated Speed ($141.0$ RPM)')

# Annotations
ax.annotate('Rated Operating Point:\n$f_{1f} = 8.30$ Hz\n3P = 7.05 Hz\nMargin = +17.7% (SAFE)',
            xy=(141.0, 8.30), xytext=(90, 18),
            arrowprops=dict(facecolor='#0066cc', shrink=0.08, width=1.5, headwidth=6),
            fontsize=9.5, fontweight='bold', bbox=dict(boxstyle='round,pad=0.5', facecolor='#e6f2ff', edgecolor='#0066cc'))

ax.set_title('Campbell Diagram: 10 kW HAWT Rotor Blade Dynamics & Resonance Margin', fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel('Rotor Rotational Speed [RPM]', fontsize=11, fontweight='bold')
ax.set_ylabel('Frequency [Hz]', fontsize=11, fontweight='bold')
ax.set_xlim(0, 180)
ax.set_ylim(0, 40)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='upper left', frameon=True, fontsize=9.5)

plt.tight_layout()
fig2_path = "reports/portfolio_figures/fig2_blade_campbell_diagram.png"
fig.savefig(fig2_path)
plt.close(fig)
print(f"[2/2] Figure 2 saved to: {fig2_path}")

print("All portfolio figures generated successfully in reports/portfolio_figures/!")
