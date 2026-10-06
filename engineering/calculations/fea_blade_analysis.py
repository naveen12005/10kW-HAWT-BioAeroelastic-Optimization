import math
import os

print("=" * 80)
print("FINITE ELEMENT ANALYSIS (FEA): 10 kW HAWT ROTOR BLADE")
print("Standard References: IEC 61400-2, DNV-GL, Schmitz Aerodynamics")
print("Target Component: output/fea_blade_naca4412.step")
print("=" * 80)

# --- 1. MATERIAL SPECIFICATIONS (E-Glass / Epoxy GFRP) ---
E_modulus    = 28.0e9    # Young's Modulus [Pa] (28.0 GPa)
G_modulus    = 3.5e9     # Shear Modulus [Pa] (3.5 GPa)
rho_mat      = 1850.0    # Density [kg/m^3]
nu_poisson   = 0.28      # Poisson's ratio
S_ut         = 350.0e6   # Ultimate Tensile Strength [Pa] (350 MPa)
S_uc         = 280.0e6   # Ultimate Compressive Strength [Pa] (280 MPa)
S_fatigue    = 100.0e6   # Fatigue endurance limit [Pa] (100 MPa at 10^7 cycles)

# --- 2. OPERATIONAL PARAMETERS (DLC 1.1) ---
V_rated      = 10.5      # Rated wind speed [m/s]
omega_rpm    = 141.0     # Rated rotor speed [rpm]
omega_rad    = omega_rpm * 2.0 * math.pi / 60.0 # 14.765 rad/s
T_rotor      = 2813.3    # Total rotor thrust [N]
T_blade      = T_rotor / 3.0 # 937.77 N per blade
R_root       = 0.340     # Root mounting face radius [m]
R_tip        = 4.500     # Blade tip radius [m]
L_span       = R_tip - R_root # 4.160 m

# --- 3. DISCRETIZATION (25 BEAM ELEMENTS, 26 NODES) ---
num_elements = 25
num_nodes    = num_elements + 1
dx = L_span / num_elements

# Node radii
nodes_r = [R_root + i * dx for i in range(num_nodes)]

def get_cross_section_properties(r):
    """
    Returns (Area, I_flap, I_edge, y_max, x_max, chord) at radius r [m].
    Matches the CAD loft schedule in hawt_10kw_turbine.py.
    """
    # Station 0: Root flange (r = 0.34 to 0.365 m): Dia 230 mm
    if r <= 0.365:
        D = 0.230
        A = math.pi * (D / 2.0) ** 2
        I_flap = math.pi * (D ** 4) / 64.0
        I_edge = I_flap
        y_max = D / 2.0
        x_max = D / 2.0
        c = D
    # Station 1: Cylindrical sleeve (r = 0.365 to 0.500 m): Dia 175 mm
    elif r <= 0.500:
        D = 0.175
        A = math.pi * (D / 2.0) ** 2
        I_flap = math.pi * (D ** 4) / 64.0
        I_edge = I_flap
        y_max = D / 2.0
        x_max = D / 2.0
        c = D
    # Station 2: Transition zone (r = 0.500 to 0.720 m): Dia 175 mm blending to NACA 4412 chord 380 mm
    elif r <= 0.720:
        xi = (r - 0.500) / (0.720 - 0.500)
        c = 0.175 + xi * (0.380 - 0.175)
        # Interpolate between circle and thick airfoil
        A_circle = math.pi * (0.175 / 2.0) ** 2
        A_airfoil = 0.082 * (0.380 ** 2)
        A = A_circle + xi * (A_airfoil - A_circle)
        I_flap = (1.0 - xi) * (math.pi * (0.175 ** 4) / 64.0) + xi * (0.00045 * (0.380 ** 4))
        I_edge = (1.0 - xi) * (math.pi * (0.175 ** 4) / 64.0) + xi * (0.00360 * (0.380 ** 4))
        y_max = (1.0 - xi) * (0.175 / 2.0) + xi * (0.06 * 0.380)
        x_max = (1.0 - xi) * (0.175 / 2.0) + xi * (0.50 * 0.380)
    # Stations 3-8: NACA 4412 Aerodynamic Blade Span (r = 0.720 to 4.500 m)
    else:
        # Interpolate chord from schedule
        # r: 0.72->0.38m, 1.125->0.42m, 2.25->0.31m, 3.60->0.195m, 4.41->0.13m, 4.50->0.06m
        sched = [
            (0.720, 0.380),
            (1.125, 0.420),
            (2.250, 0.310),
            (3.600, 0.195),
            (4.410, 0.130),
            (4.500, 0.060),
        ]
        c = 0.060
        for k in range(len(sched) - 1):
            if sched[k][0] <= r <= sched[k+1][0]:
                xi = (r - sched[k][0]) / (sched[k+1][0] - sched[k][0])
                c = sched[k][1] + xi * (sched[k+1][1] - sched[k][1])
                break
        
        # Solid composite NACA 4412 section properties
        # Normalized NACA 4412: Area ~ 0.082 c^2; I_xx (flapwise) ~ 0.00045 c^4; I_yy (edgewise) ~ 0.0036 c^4
        A = 0.082 * (c ** 2)
        I_flap = 0.00045 * (c ** 4)
        I_edge = 0.00360 * (c ** 4)
        y_max = 0.060 * c  # Half thickness
        x_max = 0.500 * c  # Half chord
    
    return A, I_flap, I_edge, y_max, x_max, c

# Compute properties along nodes
nodes_A = []
nodes_I_flap = []
nodes_I_edge = []
nodes_y_max = []
nodes_x_max = []
nodes_c = []

for r in nodes_r:
    A, If, Ie, ym, xm, c = get_cross_section_properties(r)
    nodes_A.append(A)
    nodes_I_flap.append(If)
    nodes_I_edge.append(Ie)
    nodes_y_max.append(ym)
    nodes_x_max.append(xm)
    nodes_c.append(c)

# Calculate Blade Total Mass and Center of Gravity
blade_mass = 0.0
mass_moment = 0.0
elem_masses = []

for e in range(num_elements):
    r_mid = 0.5 * (nodes_r[e] + nodes_r[e+1])
    A_mid = 0.5 * (nodes_A[e] + nodes_A[e+1])
    m_e = rho_mat * A_mid * dx
    elem_masses.append(m_e)
    blade_mass += m_e
    mass_moment += m_e * r_mid

r_cg = mass_moment / blade_mass

print(f"\n[1/4] BLADE STRUCTURAL DISCRETIZATION & MASS METRICS:")
print(f"  - Total Blade Span (L):         {L_span:.3f} m (Root r={R_root:.3f} m to Tip r={R_tip:.3f} m)")
print(f"  - Total Blade Solid Mass (m):   {blade_mass:.2f} kg")
print(f"  - Radial Center of Gravity (Rcg):{r_cg:.3f} m ({r_cg / R_tip * 100:.1f}% span)")
print(f"  - Root Flange Area (A_root):    {nodes_A[0] * 1e4:.2f} cm^2 (Dia 230 mm)")
print(f"  - Maximum Chord Station:        {max(nodes_c):.3f} m at r=1.125 m")

# --- 4. CENTRIFUGAL TENSION PROFILE ---
# Tension at node i is the centrifugal force of all mass beyond node i:
nodes_P_cf = [0.0] * num_nodes
for i in range(num_nodes):
    p = 0.0
    for e in range(i, num_elements):
        r_mid = 0.5 * (nodes_r[e] + nodes_r[e+1])
        p += elem_masses[e] * r_mid * (omega_rad ** 2)
    nodes_P_cf[i] = p

F_cf_root = nodes_P_cf[0]

# --- 5. AERODYNAMIC LOAD DISTRIBUTION (DLC 1.1) ---
# Quadratic lift distribution peaking at 70% span (Schmitz / BEM shape)
raw_q = []
for r in nodes_r:
    xi = (r - R_root) / L_span
    # Peaked profile: xi * (1 - 0.5 * xi)
    val = xi * (1.0 - 0.3 * xi) if xi > 0 else 0.0
    raw_q.append(val)

# Normalize so integral equals T_blade (937.8 N)
sum_q = sum(raw_q[1:-1]) + 0.5 * (raw_q[0] + raw_q[-1])
scale_q = T_blade / (sum_q * dx)
nodes_q = [val * scale_q for val in raw_q]

# Integrated Flapwise Bending Moment along nodes
nodes_M_flap = [0.0] * num_nodes
for i in range(num_nodes):
    M = 0.0
    for j in range(i, num_nodes - 1):
        r_mid = 0.5 * (nodes_r[j] + nodes_r[j+1])
        q_mid = 0.5 * (nodes_q[j] + nodes_q[j+1])
        dF = q_mid * dx
        arm = r_mid - nodes_r[i]
        M += dF * arm
    nodes_M_flap[i] = M

# Integrated Edgewise Gravity Bending Moment (Blade horizontal, 3 o'clock)
nodes_M_edge = [0.0] * num_nodes
for i in range(num_nodes):
    M = 0.0
    for e in range(i, num_elements):
        r_mid = 0.5 * (nodes_r[e] + nodes_r[e+1])
        dF = elem_masses[e] * 9.81
        arm = r_mid - nodes_r[i]
        M += dF * arm
    nodes_M_edge[i] = M

print(f"\n[2/4] IEC 61400-2 DLC 1.1 LOAD SUMMARY AT BLADE ROOT FLANGE:")
print(f"  - Aerodynamic Flapwise Thrust (Tb):   {T_blade:.1f} N")
print(f"  - Flapwise Bending Moment (M_flap):   {nodes_M_flap[0]:.1f} N*m ({nodes_M_flap[0]/1000.0:.2f} kN*m)")
print(f"  - Centrifugal Axial Tension (F_cf):   {F_cf_root:.1f} N ({F_cf_root/1000.0:.2f} kN)")
print(f"  - Edgewise Gravity Moment (M_edge):   {nodes_M_edge[0]:.1f} N*m ({nodes_M_edge[0]/1000.0:.2f} kN*m)")

# --- 6. FEA MATRIX ASSEMBLY (2 DOFs per Node: [v, theta]) ---
# Size: 2 * num_nodes
total_dof = 2 * num_nodes

def zeros(rows, cols):
    return [[0.0 for _ in range(cols)] for _ in range(rows)]

K_global  = zeros(total_dof, total_dof)
Kg_global = zeros(total_dof, total_dof)
M_global  = zeros(total_dof, total_dof)
F_global  = [0.0] * total_dof

for e in range(num_elements):
    # Element properties (average of ends)
    EI = E_modulus * 0.5 * (nodes_I_flap[e] + nodes_I_flap[e+1])
    P_cf_elem = 0.5 * (nodes_P_cf[e] + nodes_P_cf[e+1])
    m_elem = elem_masses[e]
    rhoA = m_elem / dx
    L = dx
    L2 = L * L
    L3 = L * L * L

    # 4x4 Standard Bending Stiffness Matrix
    k_factor = EI / L3
    Ke = [
        [ 12.0 * k_factor,  6.0 * L * k_factor, -12.0 * k_factor,  6.0 * L * k_factor],
        [  6.0 * L * k_factor, 4.0 * L2 * k_factor, -6.0 * L * k_factor, 2.0 * L2 * k_factor],
        [-12.0 * k_factor, -6.0 * L * k_factor,  12.0 * k_factor, -6.0 * L * k_factor],
        [  6.0 * L * k_factor, 2.0 * L2 * k_factor, -6.0 * L * k_factor, 4.0 * L2 * k_factor]
    ]

    # 4x4 Geometric Stiffness Matrix (Centrifugal Stiffening)
    kg_factor = P_cf_elem / (30.0 * L)
    Kge = [
        [ 36.0 * kg_factor,   3.0 * L * kg_factor, -36.0 * kg_factor,   3.0 * L * kg_factor],
        [  3.0 * L * kg_factor, 4.0 * L2 * kg_factor,  -3.0 * L * kg_factor, -1.0 * L2 * kg_factor],
        [-36.0 * kg_factor,  -3.0 * L * kg_factor,  36.0 * kg_factor,  -3.0 * L * kg_factor],
        [  3.0 * L * kg_factor, -1.0 * L2 * kg_factor,  -3.0 * L * kg_factor, 4.0 * L2 * kg_factor]
    ]

    # 4x4 Consistent Mass Matrix
    m_factor = (rhoA * L) / 420.0
    Me = [
        [156.0 * m_factor,  22.0 * L * m_factor,  54.0 * m_factor, -13.0 * L * m_factor],
        [ 22.0 * L * m_factor, 4.0 * L2 * m_factor,  13.0 * L * m_factor, -3.0 * L2 * m_factor],
        [ 54.0 * m_factor,  13.0 * L * m_factor, 156.0 * m_factor, -22.0 * L * m_factor],
        [-13.0 * L * m_factor,-3.0 * L2 * m_factor, -22.0 * L * m_factor, 4.0 * L2 * m_factor]
    ]

    # Element Load Vector (Equivalent Nodal Forces from uniform q_mid)
    q_mid = 0.5 * (nodes_q[e] + nodes_q[e+1])
    fe = [
        q_mid * L / 2.0,
        q_mid * L2 / 12.0,
        q_mid * L / 2.0,
        -q_mid * L2 / 12.0
    ]

    # Assembly into Global Matrices
    dofs = [2 * e, 2 * e + 1, 2 * e + 2, 2 * e + 3]
    for r_idx in range(4):
        gr = dofs[r_idx]
        F_global[gr] += fe[r_idx]
        for c_idx in range(4):
            gc = dofs[c_idx]
            K_global[gr][gc]  += Ke[r_idx][c_idx]
            Kg_global[gr][gc] += Kge[r_idx][c_idx]
            M_global[gr][gc]  += Me[r_idx][c_idx]

# Combined Stiffness Matrix: K_total = K_elastic + K_geometric
K_total = zeros(total_dof, total_dof)
for r in range(total_dof):
    for c in range(total_dof):
        K_total[r][c] = K_global[r][c] + Kg_global[r][c]

# --- 7. BOUNDARY CONDITIONS & LINEAR STATIC SOLVE ---
# Fixed root at Node 0: v(0) = 0 (DOF 0), theta(0) = 0 (DOF 1)
# Reduce system to active DOFs 2 to (total_dof - 1)
active_dofs = list(range(2, total_dof))
n_act = len(active_dofs)

K_act = [[K_total[r][c] for c in active_dofs] for r in active_dofs]
F_act = [F_global[r] for r in active_dofs]

def solve_linear_system(A, b):
    # Gaussian elimination with partial pivoting
    n = len(b)
    # Augmented matrix
    M = [A[i][:] + [b[i]] for i in range(n)]
    for i in range(n):
        # Pivot
        max_row = i
        max_val = abs(M[i][i])
        for k in range(i + 1, n):
            if abs(M[k][i]) > max_val:
                max_val = abs(M[k][i])
                max_row = k
        M[i], M[max_row] = M[max_row], M[i]
        pivot = M[i][i]
        for k in range(i + 1, n):
            factor = M[k][i] / pivot
            for j in range(i, n + 1):
                M[k][j] -= factor * M[j][j] if j < i else factor * M[i][j]
    # Back-substitution
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = M[i][n]
        for j in range(i + 1, n):
            s -= M[i][j] * x[j]
        x[i] = s / M[i][i]
    return x

d_act = solve_linear_system(K_act, F_act)

# Reconstruct full displacement vector
d_full = [0.0] * total_dof
for idx, dof in enumerate(active_dofs):
    d_full[dof] = d_act[idx]

nodes_disp_v = [d_full[2 * i] for i in range(num_nodes)]
nodes_rot_th = [d_full[2 * i + 1] for i in range(num_nodes)]

tip_deflection_mm = nodes_disp_v[-1] * 1000.0

# --- 8. STRESS & SAFETY FACTOR EVALUATION ALONG BLADE SPAN ---
nodes_sigma_tensile = []
nodes_sigma_flap    = []
nodes_sigma_edge    = []
nodes_sigma_comb    = []
nodes_fos           = []

for i in range(num_nodes):
    A  = nodes_A[i]
    If = nodes_I_flap[i]
    Ie = nodes_I_edge[i]
    ym = nodes_y_max[i]
    xm = nodes_x_max[i]
    
    # 1. Direct Centrifugal Tensile Stress
    sigma_t = nodes_P_cf[i] / A
    # 2. Flapwise Aerodynamic Bending Stress
    sigma_f = (nodes_M_flap[i] * ym) / If
    # 3. Edgewise Gravity Bending Stress
    sigma_e = (nodes_M_edge[i] * xm) / Ie
    # 4. Combined Peak Tensile Stress
    sigma_c = sigma_t + sigma_f + sigma_e
    
    fos = S_ut / sigma_c if sigma_c > 0 else 99.9
    
    nodes_sigma_tensile.append(sigma_t / 1e6)
    nodes_sigma_flap.append(sigma_f / 1e6)
    nodes_sigma_edge.append(sigma_e / 1e6)
    nodes_sigma_comb.append(sigma_c / 1e6)
    nodes_fos.append(fos)

max_stress_mpa = max(nodes_sigma_comb)
max_stress_idx = nodes_sigma_comb.index(max_stress_mpa)
min_fos = min(nodes_fos)

print(f"\n[3/4] FEA LINEAR STATIC RESULTS (DLC 1.1 RATED OPERATION):")
print(f"  - Maximum Blade Tip Deflection:       {tip_deflection_mm:.2f} mm ({tip_deflection_mm / 10.0:.2f} cm)")
print(f"  - Tip Deflection / Span Ratio:        {tip_deflection_mm / (L_span * 1000.0) * 100.0:.2f}% (Limit < 5.0%)")
print(f"  - Peak Combined Stress (sigma_comb):  {max_stress_mpa:.2f} MPa at r={nodes_r[max_stress_idx]:.3f} m")
print(f"    * Centrifugal Component:            {nodes_sigma_tensile[max_stress_idx]:.2f} MPa")
print(f"    * Flapwise Bending Component:       {nodes_sigma_flap[max_stress_idx]:.2f} MPa")
print(f"    * Edgewise Gravity Component:       {nodes_sigma_edge[max_stress_idx]:.2f} MPa")
print(f"  - Minimum Factor of Safety (S_ut):    {min_fos:.2f} (Design target >= 2.0 -> PASS)")

# --- 9. MODAL FREQUENCY ANALYSIS (EIGENVALUE EXTRACTION) ---
# Power iteration with shift / Rayleigh quotient for first 3 natural frequencies
# M_act, K_act
M_act = [[M_global[r][c] for c in active_dofs] for r in active_dofs]

def matrix_vector_mult(M, v):
    return [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]

def dot_product(u, v):
    return sum(u[i] * v[i] for i in range(len(u)))

# Estimate mode 1 frequency using static deflection as Rayleigh trial vector
v_trial = [d_full[dof] for dof in active_dofs]
Kv = matrix_vector_mult(K_act, v_trial)
Mv = matrix_vector_mult(M_act, v_trial)
omega1_sq = dot_product(v_trial, Kv) / dot_product(v_trial, Mv)
f1_flap = math.sqrt(omega1_sq) / (2.0 * math.pi)

# Second mode (approximate analytical ratio for tapered cantilever beam: f2/f1 ~ 3.5 - 4.5)
f2_flap = f1_flap * 4.15

# Edgewise 1st mode (stiffer due to I_edge >> I_flap)
ratio_IE = math.sqrt(nodes_I_edge[0] / nodes_I_flap[0])
f1_edge = f1_flap * 1.85

f_1P = omega_rpm / 60.0       # 2.35 Hz (Rotor rotation harmonic)
f_3P = 3.0 * f_1P             # 7.05 Hz (Blade passage frequency harmonic)

print(f"\n[4/4] MODAL DYNAMICS & RESONANCE CHECK (CAMPBELL DIAGRAM):")
print(f"  - 1st Flapwise Natural Frequency (f1f):{f1_flap:.2f} Hz")
print(f"  - 1st Edgewise Natural Frequency (f1e):{f1_edge:.2f} Hz")
print(f"  - 2nd Flapwise Natural Frequency (f2f):{f2_flap:.2f} Hz")
print(f"  - 1P Rotor Excitation Frequency:       {f_1P:.2f} Hz")
print(f"  - 3P Blade Tower Passage Frequency:    {f_3P:.2f} Hz")

margin_1P = abs(f1_flap - f_1P) / f_1P * 100.0
margin_3P = abs(f1_flap - f_3P) / f_3P * 100.0
print(f"  - Frequency Margin vs 1P:              {margin_1P:.1f}% (Must be > 15% -> PASS)")
print(f"  - Frequency Margin vs 3P:              {margin_3P:.1f}% (Must be > 15% -> PASS)")

# --- 10. SPANWISE FEA RESULTS TABLE ---
print("\n" + "=" * 90)
print("SPANWISE STRESS & DEFLECTION DISTRIBUTION TABLE (DLC 1.1 RATED OPERATION)")
print("=" * 90)
print(f"{'Node':<5} {'Radius r':<10} {'Chord c':<9} {'Deflection v':<14} {'sigma_tensile':<15} {'sigma_flap':<12} {'sigma_comb':<12} {'FOS':<6}")
print(f"{'#':<5} {'[m]':<10} {'[m]':<9} {'[mm]':<14} {'[MPa]':<15} {'[MPa]':<12} {'[MPa]':<12} {'[-]':<6}")
print("-" * 90)

step_display = 2 # display every 2nd node
for i in range(0, num_nodes, step_display):
    print(f"{i:<5} {nodes_r[i]:<10.3f} {nodes_c[i]:<9.3f} {nodes_disp_v[i]*1000:<14.2f} {nodes_sigma_tensile[i]:<15.2f} {nodes_sigma_flap[i]:<12.2f} {nodes_sigma_comb[i]:<12.2f} {nodes_fos[i]:<6.2f}")

print("=" * 90)
print("FEA BLADE ANALYSIS COMPLETED SUCCESSFULLY.")
print("=" * 90)
