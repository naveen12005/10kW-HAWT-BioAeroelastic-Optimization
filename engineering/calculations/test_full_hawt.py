import cadquery as cq
import math
import time
import os

t0 = time.time()
print("Building complete HAWT 10 kW Wind Turbine CAD model...")

# --- PARAMETERS ---
R_rotor = 4500.0        # mm (4.5 m)
H_tower = 15000.0       # mm (15.0 m)
H_hub = H_tower + 480.0 # mm (15.48 m)
hub_y = 450.0           # mm (overhang from tower axis Y=0)

# 1. FOUNDATION & ANCHORS
print("1. Creating foundation...")
foundation = (
    cq.Workplane("XY")
    .box(3600.0, 3600.0, 800.0)
    .translate((0, 0, -400.0))
)
pedestal = (
    cq.Workplane("XY")
    .cylinder(150.0, 600.0) # r=600, h=150
    .translate((0, 0, 75.0))
)
foundation = foundation.union(pedestal)

# 2. TOWER (15 m)
print("2. Creating tower...")
tower_shell = (
    cq.Workplane("XY")
    .workplane(offset=150.0)
    .circle(400.0) # Base R=400
    .workplane(offset=H_tower)
    .circle(225.0) # Top R=225
    .loft(combine=True)
)
# Tower hollow core
tower_core = (
    cq.Workplane("XY")
    .workplane(offset=140.0)
    .circle(392.0)
    .workplane(offset=H_tower + 20.0)
    .circle(217.0)
    .loft(combine=True)
)
tower_shell = tower_shell.cut(tower_core)

# Base and Top flanges
bot_flange = (
    cq.Workplane("XY")
    .cylinder(35.0, 500.0)
    .translate((0, 0, 150.0 + 17.5))
)
top_flange = (
    cq.Workplane("XY")
    .cylinder(30.0, 280.0)
    .translate((0, 0, 150.0 + H_tower - 15.0))
)
tower = tower_shell.union(bot_flange).union(top_flange)

# 3. YAW BEARING & BEDPLATE
print("3. Creating yaw system & bedplate...")
yaw_bearing = (
    cq.Workplane("XY")
    .cylinder(80.0, 260.0)
    .translate((0, 0, 150.0 + H_tower + 40.0))
)
bedplate = (
    cq.Workplane("XY")
    .box(700.0, 1800.0, 60.0)
    .translate((0, -200.0, 150.0 + H_tower + 110.0))
)
yaw_system = yaw_bearing.union(bedplate)

# 4. DRIVETRAIN & GENERATOR (PMG)
print("4. Creating drivetrain & generator...")
# Main shaft along Y axis at H_hub
# Flange at Y = hub_y - 70
shaft_flange = (
    cq.Workplane("XZ")
    .cylinder(28.0, 90.0) # r=90, h=28
    .translate((0, hub_y - 70.0 + 14.0, H_hub))
)
shaft_body = (
    cq.Workplane("XZ")
    .cylinder(600.0, 37.5) # r=37.5 (dia 75), h=600
    .translate((0, hub_y - 70.0 - 300.0, H_hub))
)
shaft = shaft_flange.union(shaft_body)

# Bearings
brg_front = (
    cq.Workplane("XY")
    .box(240.0, 140.0, 180.0)
    .translate((0, hub_y - 180.0, H_hub - 40.0))
)
brg_rear = (
    cq.Workplane("XY")
    .box(240.0, 120.0, 180.0)
    .translate((0, hub_y - 480.0, H_hub - 40.0))
)
drivetrain = shaft.union(brg_front).union(brg_rear)

# PMG Generator
pmg_stator = (
    cq.Workplane("XZ")
    .cylinder(340.0, 230.0) # r=230 (dia 460), len 340
    .translate((0, hub_y - 760.0, H_hub))
)
pmg_feet = (
    cq.Workplane("XY")
    .box(500.0, 320.0, 80.0)
    .translate((0, hub_y - 760.0, H_hub - 160.0))
)
pmg = pmg_stator.union(pmg_feet)

# 5. NACELLE COVER
print("5. Creating nacelle fairing...")
nacelle_cover = (
    cq.Workplane("XY")
    .box(820.0, 2200.0, 800.0)
    .translate((0, -250.0, H_hub + 20.0))
    .edges("|Z").fillet(80.0)
    .edges("|X").fillet(60.0)
)

# 6. ROTOR HUB & SPINNER
print("6. Creating rotor hub & spinner...")
hub_barrel = (
    cq.Workplane("XZ")
    .cylinder(260.0, 300.0) # r=300 (dia 600), len 260
    .translate((0, hub_y, H_hub))
)
hub_nose = (
    cq.Workplane("XZ")
    .workplane(offset=hub_y + 130.0)
    .circle(300.0)
    .workplane(offset=220.0)
    .circle(60.0)
    .loft(combine=True)
)
hub_nose_tip = (
    cq.Workplane("XZ")
    .sphere(60.0)
    .translate((0, hub_y + 350.0, H_hub))
)
hub = hub_barrel.union(hub_nose).union(hub_nose_tip)

# 7. BLADES (3 Blades with NACA 4412 lofts)
print("7. Creating 3 aerodynamic blades...")

def generate_naca4412_2d(chord, twist_deg, num_pts=16):
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

def generate_circle_2d(diam, twist_deg, num_pts=16):
    rad = diam / 2.0
    total_pts = num_pts * 2 - 2
    pts = []
    for i in range(total_pts):
        ang = 2.0 * math.pi * i / total_pts
        xp = rad * math.cos(ang)
        yp = rad * math.sin(ang)
        pts.append((xp, yp))
    return pts

# Blade stations along radial span (span along Z initially from hub center)
stations_def = [
    (300.0, "circle", 160.0, 16.0),
    (450.0, "circle", 160.0, 16.0),
    (675.0, "naca",   380.0, 14.5),
    (1125.0, "naca",  420.0, 12.0),
    (2250.0, "naca",  310.0, 6.5),
    (3600.0, "naca",  195.0, 2.0),
    (4410.0, "naca",  130.0, 0.0),
    (4500.0, "naca",   60.0, 0.0),
]

# Build Blade 1 along +Z (in XY plane, span = Z)
loft_builder = cq.Workplane("XY")
for r, ptype, size, twist in stations_def:
    if ptype == "circle":
        pts = generate_circle_2d(size, twist, num_pts=14)
    else:
        pts = generate_naca4412_2d(size, twist, num_pts=14)
    w = cq.Workplane("XY").workplane(offset=r).polyline(pts).close()
    loft_builder = loft_builder.add(w).toPending()

blade_proto = loft_builder.loft(combine=True)
print("  -> Blade prototype lofted in", round(time.time() - t0, 2), "s")

# Position 3 blades at 0, 120, 240 deg around rotor axis (Y axis at hub center)
blades = None
for angle in [0.0, 120.0, 240.0]:
    b = (
        blade_proto
        .rotate((0, 0, 0), (0, 1, 0), angle)
        .translate((0, hub_y, H_hub))
    )
    if blades is None:
        blades = b
    else:
        blades = blades.union(b)

print("8. Combining full assembly...")
# Combine all turbine parts into a unified master model
turbine = (
    foundation
    .union(tower)
    .union(yaw_system)
    .union(nacelle_cover)
    .union(drivetrain)
    .union(pmg)
    .union(hub)
    .union(blades)
)

shape = turbine.val()
print("Total assembly completed in", round(time.time() - t0, 2), "s")
print(f"Assembly IsValid: {shape.isValid()}")
print(f"Volume: {abs(shape.Volume()):.2f} mm^3")
bb = shape.BoundingBox()
print(f"Bounding Box: {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm")
print(f"X: [{bb.xmin:.1f}, {bb.xmax:.1f}], Y: [{bb.ymin:.1f}, {bb.ymax:.1f}], Z: [{bb.zmin:.1f}, {bb.zmax:.1f}]")

# Export STEP file
os.makedirs("output", exist_ok=True)
step_path = "output/hawt_10kw_turbine.step"
print(f"Exporting to {step_path}...")
cq.exporters.export(turbine, step_path)
print(f"STEP export finished! File size: {os.path.getsize(step_path)} bytes")
