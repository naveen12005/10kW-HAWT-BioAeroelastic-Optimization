import cadquery as cq
import math
import time
import os

# ==============================================================================
# Design: 10 kW Horizontal-Axis Wind Turbine (HAWT) Complete Engineering Model
# Target Application: Siemens NX / Siemens Designcenter (Manual STEP Import)
# Standard References: IEC 61400-2 (Small Wind Turbines), ASME B106.1M, Eurocode 3
# Output: output/hawt_10kw_turbine.step
# ==============================================================================

t0 = time.time()
print("=" * 80)
print("GENERATING HAWT 10 kW CAD MODEL (TRUE HELICAL THREADS & ROTATABLE BLADES)")
print("=" * 80)

# --- 1. PARAMETRIC ENGINEERING DIMENSIONS & ROTATION CONTROLS ---
R_rotor           = 4500.0   # Rotor radius [mm] (Diameter D = 9.0 m)
H_tower           = 15000.0  # Tower shell height [mm] (15.0 m)
H_pedestal        = 150.0    # Concrete pedestal height [mm]
tower_base_z      = H_pedestal # 150.0 mm
tower_top_z       = tower_base_z + H_tower # 15150.0 mm
H_hub             = tower_top_z + 480.0    # Rotor axis center height [mm] (15.63 m)
Y_rotor           = 520.0    # Rotor pitch axis plane along Y [mm] (forward overhang)

# Kinematic Rotation Parameters for Multi-Angle FEA & Simulation
ROTOR_AZIMUTH_DEG = 0.0      # Rotor azimuth angle [deg] (rotates complete rotor around shaft Y-axis)
BLADE_PITCH_DEG   = 0.0      # Blade pitch angle [deg] (rotates blades around longitudinal radial axis)

# Material Densities [g/mm^3]
rho_concrete      = 0.00240  # C25/30 Reinforced Concrete
rho_steel         = 0.00785  # S355 Structural Steel & 42CrMo4 Alloy Steel
rho_cast_iron     = 0.00710  # EN-GJS-400-18-LT Ductile Iron
rho_gfrp          = 0.00185  # E-Glass / Epoxy Composite

# --- 2. SUBSYSTEM 1: FOUNDATION & 16x TRUE HELICAL DRIVE ANCHOR BOLTS ---
print("[1/7] Modeling Reinforced Concrete Foundation & 16x Helical Anchor Assemblies...")
found_pad = (
    cq.Workplane("XY")
    .box(3600.0, 3600.0, 800.0)
    .translate((0, 0, -400.0))
)
pedestal = (
    cq.Workplane("XY")
    .cylinder(H_pedestal, 600.0) # radius 600 mm (dia 1200 mm)
    .translate((0, 0, H_pedestal / 2.0))
)
foundation_concrete = found_pad.union(pedestal)

# Single Prototype Stud with TRUE 3D CONTINUOUS HELICAL DRIVE THREAD (ISO 68-1 / ISO 261 M24 x 3.0)
thread_pitch = 3.0   # Standard M24 coarse thread pitch [mm]
r_maj        = 12.0  # Major diameter 24.0 mm (radius 12.0 mm)
d_cut        = 1.7   # Thread cut depth [mm]
w_cut        = 2.0 * d_cut * math.tan(math.radians(30)) # ~1.96 mm 60-degree V-cutter width
h_exposed    = 36.0  # Exposed threaded protrusion above nut [mm]

# Generate true 3D continuous helical wire path
helix_wire = cq.Wire.makeHelix(pitch=thread_pitch, height=h_exposed, radius=r_maj)

# 60-degree triangular thread cutting tool profile
cut_profile = (
    cq.Workplane("XZ")
    .polyline([(r_maj + 0.5, -w_cut / 2.0), (r_maj - d_cut, 0.0), (r_maj + 0.5, w_cut / 2.0)])
    .close()
)
helical_cutter = cut_profile.sweep(helix_wire, isFrenet=True)

# Cut continuous helical spiral teeth into cylinder blank
thread_blank = cq.Workplane("XY").cylinder(h_exposed, r_maj).translate((0, 0, h_exposed / 2.0))
threaded_tip = thread_blank.cut(helical_cutter)

# 45-degree chamfered lead-in cone at stud tip
chamfer_cutter = (
    cq.Workplane("XY")
    .workplane(offset=h_exposed - 2.5)
    .circle(r_maj + 2.0)
    .circle(r_maj)
    .workplane(offset=3.5)
    .circle(r_maj + 2.0)
    .circle(r_maj - 3.5)
    .loft(combine=True)
)
threaded_tip = threaded_tip.cut(chamfer_cutter)

# Smooth lower shank through pedestal, flange, and nut (from Z=120 to Z=208, length 88 mm)
shank_proto = cq.Workplane("XY").cylinder(88.0, r_maj).translate((0, 0, 120.0 + 44.0))

# Single prototype stud: smooth embedded shank + exposed continuous 3D helical thread
stud_proto = shank_proto.union(threaded_tip.translate((0, 0, 208.0)))

nut_s = 36.0 # M24 width across flats [mm]
d_circum = nut_s / math.cos(math.radians(30)) # 41.57 mm circumscribed diameter

all_studs = None
all_washers = None
all_nuts = None

for i in range(16):
    ang = 2.0 * math.pi * i / 16
    bx = 460.0 * math.cos(ang)
    by = 460.0 * math.sin(ang)
    
    # Stud with true continuous helical drive threads
    stud = stud_proto.translate((bx, by, 0))
    # ISO 7089 M24 Washer (resting flush on base flange from Z=185 to Z=189)
    washer = cq.Workplane("XY").cylinder(4.0, 22.0).translate((bx, by, 185.0 + 2.0))
    # ISO 4032 M24 Hex Nut (from Z=189 to Z=208)
    nut = (
        cq.Workplane("XY")
        .polygon(6, d_circum)
        .extrude(19.0)
        .translate((bx, by, 189.0))
    )
    
    if all_studs is None:
        all_studs = stud
        all_washers = washer
        all_nuts = nut
    else:
        all_studs = all_studs.union(stud)
        all_washers = all_washers.union(washer)
        all_nuts = all_nuts.union(nut)

anchor_fasteners = all_studs.union(all_washers).union(all_nuts)

# --- 3. SUBSYSTEM 2: TAPERED TUBULAR STEEL TOWER (15 m) ---
print("[2/7] Modeling 15 m Tapered Tubular Tower & Flanges (Base OD 800mm -> Top OD 450mm)...")
tower_outer = (
    cq.Workplane("XY")
    .workplane(offset=tower_base_z)
    .circle(400.0)
    .workplane(offset=H_tower)
    .circle(225.0)
    .loft(combine=True)
)
tower_inner = (
    cq.Workplane("XY")
    .workplane(offset=tower_base_z - 10.0)
    .circle(392.0)
    .workplane(offset=H_tower + 20.0)
    .circle(217.0)
    .loft(combine=True)
)
tower_shell = tower_outer.cut(tower_inner)

flange_bot = cq.Workplane("XY").cylinder(35.0, 500.0).translate((0, 0, tower_base_z + 17.5))
flange_bot = flange_bot.cut(cq.Workplane("XY").cylinder(40.0, 392.0).translate((0, 0, tower_base_z + 17.5)))

flange_top = cq.Workplane("XY").cylinder(30.0, 280.0).translate((0, 0, tower_top_z - 15.0))
flange_top = flange_top.cut(cq.Workplane("XY").cylinder(40.0, 217.0).translate((0, 0, tower_top_z - 15.0)))

tower_full = tower_shell.union(flange_bot).union(flange_top)

# --- 4. SUBSYSTEM 3: YAW SYSTEM & NACELLE BEDPLATE ---
print("[3/7] Modeling Yaw Slewing Bearing & Heavy Bedplate...")
yaw_bearing_z = tower_top_z + 40.0
yaw_bearing = cq.Workplane("XY").cylinder(80.0, 260.0).translate((0, 0, yaw_bearing_z))
bedplate_z = yaw_bearing_z + 40.0 + 30.0 # 15260 mm
bedplate = cq.Workplane("XY").box(720.0, 1600.0, 60.0).translate((0, -350.0, bedplate_z))
yaw_system = yaw_bearing.union(bedplate)

# --- 5. SUBSYSTEM 4: DRIVETRAIN & PERMANENT MAGNET GENERATOR ---
print("[4/7] Modeling Main Rotor Shaft (Dia 75mm), Bearings & PMG...")
shaft_flange_y = 390.0
shaft_flange = (
    cq.Workplane(cq.Plane(origin=(0, shaft_flange_y, H_hub), normal=(0, 1, 0)))
    .cylinder(30.0, 105.0) # Dia 210 mm, t = 30 mm
)
shaft_body = (
    cq.Workplane(cq.Plane(origin=(0, shaft_flange_y - 450.0, H_hub), normal=(0, 1, 0)))
    .cylinder(900.0, 37.5) # Dia 75 mm, len = 900 mm (extends rearward to Y = -510 mm)
)
shaft = shaft_flange.union(shaft_body)

brg_front = cq.Workplane("XY").box(240.0, 140.0, 180.0).translate((0, 140.0, H_hub - 40.0))
brg_rear  = cq.Workplane("XY").box(240.0, 120.0, 180.0).translate((0, -140.0, H_hub - 40.0))
drivetrain_full = shaft.union(brg_front).union(brg_rear)

pmg_center_y = -420.0
pmg_stator = cq.Workplane(cq.Plane(origin=(0, pmg_center_y, H_hub), normal=(0, 1, 0))).cylinder(340.0, 230.0)
pmg_feet   = cq.Workplane("XY").box(520.0, 320.0, 80.0).translate((0, pmg_center_y, H_hub - 160.0))
generator_full = pmg_stator.union(pmg_feet)

# --- 6. SUBSYSTEM 5: AERODYNAMIC NACELLE HOUSING ---
print("[5/7] Modeling Sleek Aerodynamic Nacelle Canopy...")
nacelle_cover = (
    cq.Workplane("XY")
    .box(800.0, 1700.0, 720.0)
    .translate((0, -570.0, H_hub + 10.0))
    .edges("|Z").fillet(75.0)
    .edges("|X").fillet(55.0)
)
shaft_hole = cq.Workplane(cq.Plane(origin=(0, 280.0, H_hub), normal=(0, 1, 0))).cylinder(120.0, 140.0)
nacelle_cover = nacelle_cover.cut(shaft_hole)

# --- 7. SUBSYSTEM 6: ROTOR HUB & SPINNER (WITH AZIMUTH ROTATION SUPPORT) ---
print("[6/7] Modeling Rotor Hub & Spinner Dome (Azimuth Angle = {:.1f} deg)...".format(ROTOR_AZIMUTH_DEG))
hub_barrel_proto = cq.Workplane(cq.Plane(origin=(0, 440.0 - Y_rotor, 0), normal=(0, 1, 0))).cylinder(240.0, 280.0)
hub_nose_proto = (
    cq.Workplane(cq.Plane(origin=(0, 560.0 - Y_rotor, 0), normal=(0, 1, 0)))
    .circle(280.0)
    .workplane(offset=240.0)
    .circle(180.0)
    .workplane(offset=180.0)
    .circle(60.0)
    .loft(combine=True)
)
hub_nose_tip_proto = cq.Workplane(cq.Plane(origin=(0, 980.0 - Y_rotor, 0), normal=(0, 1, 0))).sphere(60.0)

boss_base = cq.Workplane("XY").cylinder(95.0, 115.0).translate((0, 0, 267.5))
boss_flange = cq.Workplane("XY").cylinder(25.0, 125.0).translate((0, 0, 327.5))
boss_proto = boss_base.union(boss_flange)

pitch_bolts = None
for i in range(12):
    ang = 2.0 * math.pi * i / 12
    bx = 105.0 * math.cos(ang)
    by = 105.0 * math.sin(ang)
    d_c = 16.0 / math.cos(math.radians(30))
    bolt = cq.Workplane("XY").polygon(6, d_c).extrude(10.0).translate((bx, by, 328.0))
    if pitch_bolts is None:
        pitch_bolts = bolt
    else:
        pitch_bolts = pitch_bolts.union(bolt)

boss_full_proto = boss_proto.union(pitch_bolts)

hub_bosses_proto = None
for base_ang in [0.0, 120.0, 240.0]:
    b = boss_full_proto.rotate((0, 0, 0), (0, 1, 0), base_ang)
    if hub_bosses_proto is None:
        hub_bosses_proto = b
    else:
        hub_bosses_proto = hub_bosses_proto.union(b)

hub_raw = hub_barrel_proto.union(hub_nose_proto).union(hub_nose_tip_proto).union(hub_bosses_proto)
# Apply Rotor Azimuth Rotation around Y-axis, then translate to hub elevation
hub_full = hub_raw.rotate((0, 0, 0), (0, 1, 0), ROTOR_AZIMUTH_DEG).translate((0, Y_rotor, H_hub))

# --- 8. SUBSYSTEM 7: 3 AERODYNAMIC BLADES (WITH INDEPENDENT PITCH & AZIMUTH ROTATION) ---
print("[7/7] Modeling 3 Rotatable Aerodynamic Blades (Pitch = {:.1f} deg, Azimuth = {:.1f} deg)...".format(BLADE_PITCH_DEG, ROTOR_AZIMUTH_DEG))

def generate_naca4412_points(chord, twist_deg, num_pts=14):
    m = 0.04
    p = 0.40
    t = 0.12
    beta_vals = [math.pi * i / (num_pts - 1) for i in range(num_pts)]
    xc_vals = [0.5 * (1.0 - math.cos(b)) for b in beta_vals]
    upper = []
    lower = []
    for xc in xc_vals:
        yt = 5.0 * t * (
            0.2969 * math.sqrt(xc)
            - 0.1260 * xc
            - 0.3516 * (xc ** 2)
            + 0.2843 * (xc ** 3)
            - 0.1036 * (xc ** 4)
        )
        if p > 0:
            if xc < p:
                yc = (m / (p ** 2)) * (2.0 * p * xc - (xc ** 2))
                dy_dx = (2.0 * m / (p ** 2)) * (p - xc)
            else:
                yc = (m / ((1.0 - p) ** 2)) * ((1.0 - 2.0 * p) + 2.0 * p * xc - (xc ** 2))
                dy_dx = (2.0 * m / ((1.0 - p) ** 2)) * (p - xc)
            theta = math.atan(dy_dx)
        else:
            yc = 0.0
            theta = 0.0
        xu = (xc - yt * math.sin(theta)) * chord
        yu = (yc + yt * math.cos(theta)) * chord
        xl = (xc + yt * math.sin(theta)) * chord
        yl = (yc - yt * math.cos(theta)) * chord
        upper.append((xu, yu))
        lower.append((xl, yl))
    local_pts = []
    for pt in reversed(upper):
        local_pts.append(pt)
    for pt in lower[1:-1]:
        local_pts.append(pt)
    twist_rad = math.radians(twist_deg)
    cos_t = math.cos(twist_rad)
    sin_t = math.sin(twist_rad)
    transformed_pts = []
    for (lx, ly) in local_pts:
        xp = lx - 0.25 * chord
        yp = ly
        xr = xp * cos_t - yp * sin_t
        yr = xp * sin_t + yp * cos_t
        transformed_pts.append((xr, yr))
    return transformed_pts

def generate_circle_points(diam, twist_deg, num_pts=14):
    rad = diam / 2.0
    total_pts = num_pts * 2 - 2
    pts = []
    for i in range(total_pts):
        ang = 2.0 * math.pi * i / total_pts
        xp = rad * math.cos(ang)
        yp = rad * math.sin(ang)
        pts.append((xp, yp))
    return pts

stations_schedule = [
    (340.0,  "circle", 230.0, 16.0), # Flange face matching hub boss
    (365.0,  "circle", 230.0, 16.0), # Flange thickness 25 mm
    (500.0,  "circle", 175.0, 16.0), # Revolute root cylindrical sleeve
    (720.0,  "naca",   380.0, 15.0), # Transition to thick NACA 4412
    (1125.0, "naca",   420.0, 12.0), # Maximum chord station
    (2250.0, "naca",   310.0, 6.5),  # Mid-span station
    (3600.0, "naca",   195.0, 2.0),  # Outer span station
    (4410.0, "naca",   130.0, 0.0),  # Near tip station
    (4500.0, "naca",    60.0, 0.0),  # Tip cap station
]

current_z = 0.0
loft_wp = cq.Workplane("XY")

for r, ptype, size, twist in stations_schedule:
    delta_z = r - current_z
    current_z = r
    loft_wp = loft_wp.workplane(offset=delta_z)
    if ptype == "circle":
        pts = generate_circle_points(size, twist, num_pts=14)
    else:
        pts = generate_naca4412_points(size, twist, num_pts=14)
    loft_wp = loft_wp.polyline(pts).close()

blade_proto = loft_wp.loft(combine=True)

# Apply Blade Pitch Rotation about each blade's longitudinal radial axis (Z-axis)
blade_pitched = blade_proto.rotate((0, 0, 0), (0, 0, 1), BLADE_PITCH_DEG)

# 3 Individual, Rotatable Blades positioned in rotor plane with Azimuth angle
blade_1 = blade_pitched.rotate((0, 0, 0), (0, 1, 0), 0.0 + ROTOR_AZIMUTH_DEG).translate((0, Y_rotor, H_hub))
blade_2 = blade_pitched.rotate((0, 0, 0), (0, 1, 0), 120.0 + ROTOR_AZIMUTH_DEG).translate((0, Y_rotor, H_hub))
blade_3 = blade_pitched.rotate((0, 0, 0), (0, 1, 0), 240.0 + ROTOR_AZIMUTH_DEG).translate((0, Y_rotor, H_hub))

# --- 9. BUILD COMPLETE CADQUERY ASSEMBLY ---
print("Assembling complete HAWT system...")
assy = cq.Assembly()
assy.add(foundation_concrete, name="Foundation_Reinforced_Concrete", color=cq.Color(0.68, 0.68, 0.65))
assy.add(anchor_fasteners, name="Anchor_Helical_Bolts_Washers_Nuts_16x_M24", color=cq.Color(0.25, 0.25, 0.28))
assy.add(tower_full, name="Tower_Tubular_Steel_15m", color=cq.Color(0.85, 0.85, 0.87))
assy.add(yaw_system, name="Yaw_Bearing_and_Bedplate", color=cq.Color(0.35, 0.38, 0.42))
assy.add(drivetrain_full, name="Main_Shaft_and_Bearing_Units", color=cq.Color(0.72, 0.72, 0.76))
assy.add(generator_full, name="Direct_Drive_PMG_Generator", color=cq.Color(0.18, 0.42, 0.78))
assy.add(nacelle_cover, name="Nacelle_Aerodynamic_Canopy", color=cq.Color(0.94, 0.94, 0.94))
assy.add(hub_full, name="Rotor_Hub_and_Spinner_Dome", color=cq.Color(0.88, 0.20, 0.15))
assy.add(blade_1, name="Blade_01_NACA4412_Rotatable", color=cq.Color(0.97, 0.97, 0.97))
assy.add(blade_2, name="Blade_02_NACA4412_Rotatable", color=cq.Color(0.97, 0.97, 0.97))
assy.add(blade_3, name="Blade_03_NACA4412_Rotatable", color=cq.Color(0.97, 0.97, 0.97))

# --- 10. EXPORT STEP FILE ---
os.makedirs("output", exist_ok=True)
step_path = "output/hawt_10kw_turbine.step"
print(f"Exporting full assembly to STEP format: {step_path}...")
assy.save(step_path)
file_size_bytes = os.path.getsize(step_path)
file_size_mb = file_size_bytes / (1024 * 1024)

# --- 11. PHYSICAL & GEOMETRIC TELEMETRY ---
v_foundation = abs(foundation_concrete.val().Volume())
v_fasteners  = abs(anchor_fasteners.val().Volume())
v_tower      = abs(tower_full.val().Volume())
v_yaw        = abs(yaw_system.val().Volume())
v_drivetrain = abs(drivetrain_full.val().Volume())
v_generator  = abs(generator_full.val().Volume())
v_nacelle    = abs(nacelle_cover.val().Volume())
v_hub        = abs(hub_full.val().Volume())
v_blade      = abs(blade_proto.val().Volume())
v_3blades    = v_blade * 3.0

total_volume_mm3 = (
    v_foundation + v_fasteners + v_tower + v_yaw + v_drivetrain +
    v_generator + v_nacelle + v_hub + v_3blades
)

# Masses in kg
m_foundation_kg = v_foundation * rho_concrete / 1000.0
m_fasteners_kg  = v_fasteners * rho_steel / 1000.0
m_tower_kg      = v_tower * rho_steel / 1000.0
m_yaw_kg        = v_yaw * rho_steel / 1000.0
m_drivetrain_kg = v_drivetrain * rho_steel / 1000.0
m_generator_kg  = v_generator * rho_steel / 1000.0
m_nacelle_kg    = v_nacelle * rho_gfrp / 1000.0
m_hub_kg        = v_hub * rho_cast_iron / 1000.0
m_blade_kg      = v_blade * rho_gfrp / 1000.0
m_3blades_kg    = m_blade_kg * 3.0

m_rotor_kg      = m_hub_kg + m_3blades_kg
m_top_head_kg   = m_rotor_kg + m_drivetrain_kg + m_generator_kg + m_yaw_kg + m_nacelle_kg
m_turbine_kg    = m_top_head_kg + m_tower_kg + m_fasteners_kg
m_total_kg      = m_turbine_kg + m_foundation_kg

# Bounding box of full envelope
x_len = 2.0 * R_rotor # 9000 mm
y_len = 1040.0 - (-1420.0) # 2460 mm
z_len = (H_hub + R_rotor) - (-800.0) # 20130 - (-800) = 20930 mm

print("\n" + "=" * 80)
print("=== CAD Design Telemetry: hawt_10kw_turbine ===")
print("=" * 80)
print(f"Full STEP File Path:  {os.path.abspath(step_path)}")
print(f"STEP File Size:       {file_size_bytes} bytes ({file_size_mb:.2f} MB)")
print(f"Total CAD Volume:     {total_volume_mm3:.2f} mm^3 ({total_volume_mm3 / 1e9:.4f} m^3)")
print(f"Overall Bounding Box: {x_len:.1f} (X) x {y_len:.1f} (Y) x {z_len:.1f} (Z) mm")
print(f"Rotor Diameter:       {2.0 * R_rotor:.1f} mm (9.0 m)")
print(f"Hub Height:           {H_hub:.1f} mm (15.63 m above ground)")
print(f"Total Blade Tip Reach:{H_hub + R_rotor:.1f} mm (20.13 m maximum tip height)")
print(f"Kinematic State:      Azimuth = {ROTOR_AZIMUTH_DEG:.1f} deg, Pitch = {BLADE_PITCH_DEG:.1f} deg")
print("-" * 80)
print("SUBSYSTEM COMPONENT MASS BREAKDOWN:")
print(f"  - 3x Rotatable Blades (GFRP):          {m_3blades_kg:.1f} kg ({m_blade_kg:.1f} kg/blade)")
print(f"  - Rotor Hub & Nose Spinner (Cast Iron):{m_hub_kg:.1f} kg")
print(f"  - Rotor Subsystem Total Mass:          {m_rotor_kg:.1f} kg")
print(f"  - Main Shaft & Bearing Units (Steel):  {m_drivetrain_kg:.1f} kg")
print(f"  - Direct-Drive PMG Generator:          {m_generator_kg:.1f} kg")
print(f"  - Yaw Bearing & Bedplate Frame:        {m_yaw_kg:.1f} kg")
print(f"  - Nacelle Canopy Fairing (GFRP):       {m_nacelle_kg:.1f} kg")
print(f"  - Tower Head Assembly (Top Mass):      {m_top_head_kg:.1f} kg")
print(f"  - Tubular Steel Tower Shell (15 m):    {m_tower_kg:.1f} kg")
print(f"  - 16x Helical Anchor Bolt Assemblies:  {m_fasteners_kg:.1f} kg")
print(f"  - Turbine Total Dry Weight:            {m_turbine_kg:.1f} kg ({m_turbine_kg / 1000.0:.2f} tonnes)")
print(f"  - Foundation Reinforced Concrete:      {m_foundation_kg:.1f} kg ({m_foundation_kg / 1000.0:.2f} tonnes)")
print(f"  - Total Installed System Mass:         {m_total_kg:.1f} kg ({m_total_kg / 1000.0:.2f} tonnes)")
print("=" * 80)
print(f"Execution completed successfully in {time.time() - t0:.2f} seconds.")
print("=" * 80)
