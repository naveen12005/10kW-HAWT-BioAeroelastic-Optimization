import cadquery as cq
import math

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
    (300.0,  "circle", 160.0, 16.0),
    (450.0,  "circle", 160.0, 16.0),
    (675.0,  "naca",   380.0, 14.5),
    (1125.0, "naca",   420.0, 12.0),
    (2250.0, "naca",   310.0, 6.5),
    (3600.0, "naca",   195.0, 2.0),
    (4410.0, "naca",   130.0, 0.0),
    (4500.0, "naca",    60.0, 0.0),
]

base_wp = cq.Workplane("XY")
loft_builder = cq.Workplane("XY")

for r, ptype, size, twist in stations_schedule:
    if ptype == "circle":
        pts = generate_circle_points(size, twist, num_pts=14)
    else:
        pts = generate_naca4412_points(size, twist, num_pts=14)
    # Correct absolute offset from base plane
    w = base_wp.workplane(offset=r).polyline(pts).close()
    loft_builder = loft_builder.add(w).toPending()

blade_proto = loft_builder.loft(combine=True)
bb = blade_proto.val().BoundingBox()
vol = abs(blade_proto.val().Volume())
print(f"Blade Bounding Box: {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm")
print(f"Z span: {bb.zmin:.1f} to {bb.zmax:.1f} mm (Expected 300 to 4500 mm)")
print(f"Solid Volume: {vol:.1f} mm^3 = {vol/1e6:.3f} liters ({vol/1e9:.5f} m^3)")
# Real hollow composite blade mass (equivalent shell thickness ~ 4 mm):
# Surface area ~ 2 * 4.2 * 0.28 ~ 2.35 m^2 * 0.004 m * 1850 kg/m^3 ~ 17.4 kg + spar ~ 28 kg!
print(f"Solid Volume mass (if 100% solid GFRP): {vol * 0.00185 / 1000.0:.2f} kg")
