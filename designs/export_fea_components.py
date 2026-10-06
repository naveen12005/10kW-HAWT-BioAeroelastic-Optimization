import cadquery as cq
import math
import time
import os

print("=" * 80)
print("EXPORTING ISOLATED HAWT COMPONENTS FOR FEA ANALYSIS")
print("=" * 80)

# --- BLADE GEOMETRY DEFINITION ---
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

blade_solid = loft_wp.loft(combine=True)

# Export Blade
os.makedirs("output", exist_ok=True)
blade_step = "output/fea_blade_naca4412.step"
print(f"[1/3] Exporting isolated Blade to: {blade_step}...")
cq.exporters.export(blade_solid, blade_step)
print(f"  Blade STEP exported! Size: {os.path.getsize(blade_step)} bytes.")

# --- TOWER GEOMETRY DEFINITION ---
tower_base_z = 150.0
H_tower = 15000.0
tower_top_z = tower_base_z + H_tower

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

tower_solid = tower_shell.union(flange_bot).union(flange_top)

tower_step = "output/fea_tower_15m.step"
print(f"[2/3] Exporting isolated Tower to: {tower_step}...")
cq.exporters.export(tower_solid, tower_step)
print(f"  Tower STEP exported! Size: {os.path.getsize(tower_step)} bytes.")

# --- HUB & MAIN SHAFT GEOMETRY DEFINITION ---
H_hub = tower_top_z + 480.0
Y_rotor = 520.0

hub_barrel = cq.Workplane(cq.Plane(origin=(0, 440.0, H_hub), normal=(0, 1, 0))).cylinder(240.0, 280.0)
hub_nose = (
    cq.Workplane(cq.Plane(origin=(0, 560.0, H_hub), normal=(0, 1, 0)))
    .circle(280.0)
    .workplane(offset=240.0)
    .circle(180.0)
    .workplane(offset=180.0)
    .circle(60.0)
    .loft(combine=True)
)
hub_nose_tip = cq.Workplane(cq.Plane(origin=(0, 980.0, H_hub), normal=(0, 1, 0))).sphere(60.0)

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

hub_bosses = None
for base_ang in [0.0, 120.0, 240.0]:
    b = boss_full_proto.rotate((0, 0, 0), (0, 1, 0), base_ang).translate((0, Y_rotor, H_hub))
    if hub_bosses is None:
        hub_bosses = b
    else:
        hub_bosses = hub_bosses.union(b)

hub_solid = hub_barrel.union(hub_nose).union(hub_nose_tip).union(hub_bosses)

shaft_flange_y = 390.0
shaft_flange = cq.Workplane(cq.Plane(origin=(0, shaft_flange_y, H_hub), normal=(0, 1, 0))).cylinder(30.0, 105.0)
shaft_body   = cq.Workplane(cq.Plane(origin=(0, shaft_flange_y - 450.0, H_hub), normal=(0, 1, 0))).cylinder(900.0, 37.5)
shaft_solid  = shaft_flange.union(shaft_body)

hub_shaft_assembly = cq.Assembly()
hub_shaft_assembly.add(hub_solid, name="Hub_Casting", color=cq.Color(0.85, 0.20, 0.15))
hub_shaft_assembly.add(shaft_solid, name="Main_Shaft", color=cq.Color(0.70, 0.70, 0.75))

hub_shaft_step = "output/fea_hub_shaft.step"
print(f"[3/3] Exporting Hub & Main Shaft Assembly to: {hub_shaft_step}...")
hub_shaft_assembly.save(hub_shaft_step)
print(f"  Hub & Shaft STEP exported! Size: {os.path.getsize(hub_shaft_step)} bytes.")

print("=" * 80)
print("ALL FEA ISOLATED STEP GEOMETRIES EXPORTED SUCCESSFULLY!")
print("=" * 80)
