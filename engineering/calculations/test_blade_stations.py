"""
Test blade station coordinate generation
"""
import math

def generate_blade_stations():
    stations_def = [
        {"r": 300.0,  "type": "circle", "diam": 160.0, "twist": 16.0},
        {"r": 450.0,  "type": "circle", "diam": 160.0, "twist": 16.0},
        {"r": 675.0,  "type": "naca",   "chord": 380.0, "t_ratio": 0.28, "camber": 0.04, "p": 0.40, "twist": 14.5},
        {"r": 1125.0, "type": "naca",   "chord": 420.0, "t_ratio": 0.12, "camber": 0.04, "p": 0.40, "twist": 12.0},
        {"r": 1575.0, "type": "naca",   "chord": 370.0, "t_ratio": 0.12, "camber": 0.04, "p": 0.40, "twist": 9.5},
        {"r": 2250.0, "type": "naca",   "chord": 310.0, "t_ratio": 0.12, "camber": 0.04, "p": 0.40, "twist": 6.5},
        {"r": 2925.0, "type": "naca",   "chord": 250.0, "t_ratio": 0.12, "camber": 0.04, "p": 0.40, "twist": 4.0},
        {"r": 3600.0, "type": "naca",   "chord": 195.0, "t_ratio": 0.12, "camber": 0.04, "p": 0.40, "twist": 2.0},
        {"r": 4050.0, "type": "naca",   "chord": 160.0, "t_ratio": 0.12, "camber": 0.04, "p": 0.40, "twist": 0.8},
        {"r": 4410.0, "type": "naca",   "chord": 130.0, "t_ratio": 0.12, "camber": 0.04, "p": 0.40, "twist": 0.0},
        {"r": 4500.0, "type": "naca",   "chord": 60.0,  "t_ratio": 0.12, "camber": 0.02, "p": 0.40, "twist": 0.0},
    ]
    
    num_pts = 31 # Points per section
    all_sections = []
    
    for s in stations_def:
        r = s["r"]
        twist_rad = math.radians(s["twist"])
        cos_t = math.cos(twist_rad)
        sin_t = math.sin(twist_rad)
        
        pts_3d = []
        if s["type"] == "circle":
            rad = s["diam"] / 2.0
            # Generate circle points with same point count and starting angle as airfoil trailing edge (+X direction)
            for i in range(num_pts * 2 - 2):
                angle = 2.0 * math.pi * i / (num_pts * 2 - 2)
                # In 2D local plane: x' along chord, y' thickness
                x_p = rad * math.cos(angle)
                y_p = rad * math.sin(angle)
                # Rotate by twist
                x_rot = x_p * cos_t - y_p * sin_t
                z_rot = x_p * sin_t + y_p * cos_t
                pts_3d.append((x_rot, r, z_rot))
        else:
            c = s["chord"]
            m = s["camber"]
            p = s["p"]
            t = s["t_ratio"]
            
            # Cosine spacing
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
                
                xu = (xc - yt * math.sin(theta)) * c
                yu = (yc + yt * math.cos(theta)) * c
                xl = (xc + yt * math.sin(theta)) * c
                yl = (yc - yt * math.cos(theta)) * c
                upper.append((xu, yu))
                lower.append((xl, yl))
                
            local_2d = []
            # Trailing edge -> Upper surface -> Leading edge -> Lower surface -> Trailing edge
            for pt in reversed(upper):
                local_2d.append(pt)
            for pt in lower[1:-1]:
                local_2d.append(pt)
                
            for (lx, ly) in local_2d:
                # Offset pitch axis (quarter-chord)
                x_p = lx - 0.25 * c
                y_p = ly
                x_rot = x_p * cos_t - y_p * sin_t
                z_rot = x_p * sin_t + y_p * cos_t
                pts_3d.append((x_rot, r, z_rot))
                
        all_sections.append((s, pts_3d))
        print(f"Station r={r:6.1f} mm: type={s['type']:6s}, chord/diam={s.get('chord', s.get('diam')):5.1f} mm, twist={s['twist']:4.1f} deg, pts={len(pts_3d)}")

    return all_sections

if __name__ == "__main__":
    generate_blade_stations()
