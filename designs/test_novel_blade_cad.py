import cadquery as cq
import math
import os
import time

print("=" * 80)
print("TESTING 3D CAD MODELING OF NOVEL BIO-AEROELASTIC HYBRID BLADE")
print("Innovations: Leading-Edge Tubercles + Aft Swept Tip (Bend-Twist Coupling)")
print("=" * 80)

def generate_naca4412_points(chord, twist_deg, le_offset=0.0, num_pts=16):
    """
    Generates NACA 4412 airfoil coordinates with custom chord, twist, and leading-edge tubercle offset.
    le_offset > 0 shifts the leading edge forward (tubercle crest).
    le_offset < 0 recesses the leading edge (tubercle trough).
    """
    m = 0.04
    p = 0.40
    t = 0.12
    beta_vals = [math.pi * i / (num_pts - 1) for i in range(num_pts)]
    xc_vals = [0.5 * (1.0 - math.cos(b)) for b in beta_vals]
    upper = []
    lower = []
    
    # Tubercle stretch factor on leading edge (smooth decaying influence toward trailing edge)
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
            
        # Apply tubercle LE forward displacement (decays as (1-xc)^2 toward trailing edge)
        dx_tubercle = le_offset * ((1.0 - xc) ** 2)
        
        xu = (xc * chord) - dx_tubercle - (yt * math.sin(theta) * chord)
        yu = (yc + yt * math.cos(theta)) * chord
        xl = (xc * chord) - dx_tubercle + (yt * math.sin(theta) * chord)
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
    # Pitch axis at quarter-chord
    for (lx, ly) in local_pts:
        xp = lx - 0.25 * chord
        yp = ly
        xr = xp * cos_t - yp * sin_t
        yr = xp * sin_t + yp * cos_t
        transformed_pts.append((xr, yr))
        
    return transformed_pts

def generate_circle_points(diam, num_pts=16):
    rad = diam / 2.0
    total_pts = num_pts * 2 - 2
    pts = []
    for i in range(total_pts):
        ang = 2.0 * math.pi * i / total_pts
        xp = rad * math.cos(ang)
        yp = rad * math.sin(ang)
        pts.append((xp, yp))
    return pts

# --- 14 RADIAL STATIONS FOR SMOOTH LOFTING WITH TUBERCLES & SWEPT TIP ---
# Span: r = 340 mm to 4500 mm
# Tubercles active between r = 1125 mm and r = 3150 mm (wavelength lambda = 450 mm, amplitude A = 22 mm)
# Aft sweep active between r = 3150 mm and r = 4500 mm (max sweep = 120 mm)
stations_config = [
    # r (mm), type, size/chord (mm), twist (deg), LE_offset (mm), sweep_y (mm)
    (340.0,  "circle", 230.0, 16.0,   0.0,   0.0),   # Root flange face
    (365.0,  "circle", 230.0, 16.0,   0.0,   0.0),   # Flange thickness
    (500.0,  "circle", 175.0, 16.0,   0.0,   0.0),   # Cylindrical sleeve
    (720.0,  "naca",   380.0, 15.0,   0.0,   0.0),   # Transition start
    (1125.0, "naca",   420.0, 12.0, +22.0,   0.0),   # Tubercle Crest 1
    (1350.0, "naca",   390.0, 10.5, -15.0,   0.0),   # Tubercle Trough 1
    (1575.0, "naca",   365.0,  9.0, +20.0,   0.0),   # Tubercle Crest 2
    (1800.0, "naca",   345.0,  8.0, -14.0,   0.0),   # Tubercle Trough 2
    (2025.0, "naca",   325.0,  7.0, +18.0,   0.0),   # Tubercle Crest 3
    (2250.0, "naca",   310.0,  6.5, -12.0,   0.0),   # Tubercle Trough 3
    (2550.0, "naca",   285.0,  5.5, +16.0,   0.0),   # Tubercle Crest 4
    (2850.0, "naca",   255.0,  4.5, -10.0,   0.0),   # Tubercle Trough 4
    (3150.0, "naca",   230.0,  3.5,   0.0,   0.0),   # Tubercle End / Sweep Start
    (3600.0, "naca",   195.0,  2.0,   0.0, -15.0),   # Swept mid-tip
    (4050.0, "naca",   160.0,  1.0,   0.0, -45.0),   # Swept outer-tip
    (4350.0, "naca",   130.0,  0.5,   0.0, -85.0),   # Swept near-tip
    (4470.0, "naca",    90.0,  0.0,   0.0, -110.0),  # Swept winglet blend
    (4500.0, "naca",    45.0,  0.0,   0.0, -120.0),  # Swept winglet cap
]

t0 = time.time()
print("Constructing 18-station 3D solid loft with biomimetic tubercles and aft sweep...")

current_z = 0.0
loft_wp = cq.Workplane("XY")

for r, ptype, size, twist, le_off, sw_y in stations_config:
    delta_z = r - current_z
    current_z = r
    
    if ptype == "circle":
        pts = generate_circle_points(size, num_pts=16)
    else:
        pts = generate_naca4412_points(size, twist, le_offset=le_off, num_pts=16)
        
    # Offset points by aft sweep sw_y
    offset_pts = [(x, y + sw_y) for (x, y) in pts]
    
    loft_wp = loft_wp.workplane(offset=delta_z)
    loft_wp = loft_wp.polyline(offset_pts).close()

blade_novel = loft_wp.loft(combine=True)
t_loft = time.time() - t0
print(f"3D Loft successful in {t_loft:.2f} seconds!")

# Export STEP
out_step = "output/fea_novel_blade_bio_aeroelastic.step"
os.makedirs("output", exist_ok=True)
print(f"Exporting to: {out_step}...")
cq.exporters.export(blade_novel, out_step)
print(f"File exported! Size: {os.path.getsize(out_step):,} bytes.")
print("=" * 80)
