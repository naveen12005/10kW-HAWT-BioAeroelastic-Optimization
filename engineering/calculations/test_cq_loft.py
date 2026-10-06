import cadquery as cq
import math
import time

t0 = time.time()
print("Starting CadQuery blade loft test...")

def generate_naca4412_2d(chord, twist_deg, num_pts=20):
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
        zr = xp * sin_t + yp * cos_t
        transformed_pts.append((xr, zr))
    return transformed_pts

def generate_circle_2d(diam, twist_deg, num_pts=20):
    rad = diam / 2.0
    total_pts = num_pts * 2 - 2
    twist_rad = math.radians(twist_deg)
    cos_t = math.cos(twist_rad)
    sin_t = math.sin(twist_rad)
    pts = []
    for i in range(total_pts):
        ang = 2.0 * math.pi * i / total_pts
        xp = rad * math.cos(ang)
        yp = rad * math.sin(ang)
        xr = xp * cos_t - yp * sin_t
        zr = xp * sin_t + yp * cos_t
        pts.append((xr, zr))
    return pts

# Stations
stations = [
    (300.0, "circle", 160.0, 16.0),
    (450.0, "circle", 160.0, 16.0),
    (675.0, "naca", 380.0, 14.5),
    (1125.0, "naca", 420.0, 12.0),
    (2250.0, "naca", 310.0, 6.5),
    (3600.0, "naca", 195.0, 2.0),
    (4410.0, "naca", 130.0, 0.0),
    (4500.0, "naca", 60.0, 0.0),
]

wp = cq.Workplane("XZ")
wires = []
for r, ptype, size, twist in stations:
    if ptype == "circle":
        pts = generate_circle_2d(size, twist, num_pts=16)
    else:
        pts = generate_naca4412_2d(size, twist, num_pts=16)
    w = cq.Workplane("XZ").workplane(offset=r).polyline(pts).close()
    wires.append(w)

loft_builder = cq.Workplane("XZ")
for w in wires:
    loft_builder = loft_builder.add(w).toPending()

solid_blade = loft_builder.loft(combine=True)
shape = solid_blade.val()
print(f"Loft finished in {time.time() - t0:.2f} s. IsValid: {shape.isValid()}, Volume: {shape.Volume():.1f} mm^3")
