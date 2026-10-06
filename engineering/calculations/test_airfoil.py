"""
Test NACA 4412 point generator and station lofts
"""
import math

def naca4(m, p, t, c, num_points=30):
    # m = max camber (0.04 for NACA 4412)
    # p = location of max camber (0.40 for NACA 4412)
    # t = max thickness as fraction of chord (0.12 for NACA 4412)
    # c = chord length in mm
    pts = []
    # Cosine spacing for better resolution near leading edge
    beta_vals = [math.pi * i / (num_points - 1) for i in range(num_points)]
    xc_vals = [0.5 * (1.0 - math.cos(b)) for b in beta_vals]
    
    upper = []
    lower = []
    
    for xc in xc_vals:
        # Thickness
        yt = 5.0 * t * (
            0.2969 * math.sqrt(xc)
            - 0.1260 * xc
            - 0.3516 * (xc ** 2)
            + 0.2843 * (xc ** 3)
            - 0.1036 * (xc ** 4) # closed trailing edge
        )
        # Camber
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
        
    # Order points clockwise or counter-clockwise starting from trailing edge:
    # Trailing edge -> Upper surface -> Leading edge -> Lower surface -> Trailing edge
    curve_pts = []
    for pt in reversed(upper): # Trailing edge to LE along upper surface
        curve_pts.append(pt)
    for pt in lower[1:]: # LE to trailing edge along lower surface
        curve_pts.append(pt)
        
    return curve_pts

# Test generation
pts = naca4(0.04, 0.40, 0.12, 420.0, 25)
print(f"Generated {len(pts)} points for chord 420 mm.")
print(f"First point (TE): {pts[0]}")
print(f"Mid point (LE): {pts[len(pts)//2]}")
print(f"Last point (TE): {pts[-1]}")
