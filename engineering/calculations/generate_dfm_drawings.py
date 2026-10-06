import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Polygon, Arc
import numpy as np
import os

print("Generating 2D Manufacturing Drawing Sheets (ISO 1101 / ASME Y14.5)...")

os.makedirs("reports/portfolio_figures", exist_ok=True)

def draw_title_block(ax, dwg_no, title, sheet_no="1 OF 3", material="HYBRID GFRP/CFRP", tolerance="ISO 2768-mK", scale="1:25"):
    """Draws a professional ISO/DIN engineering title block at the bottom right corner."""
    # Outer frame coordinates (0 to 100, 0 to 70 normalized layout)
    # Title block in [58, 98] x [2, 16]
    tb_x0 = 55.0
    tb_y0 = 2.0
    tb_w = 43.0
    tb_h = 13.0
    
    # Outer border of title block
    ax.add_patch(patches.Rectangle((tb_x0, tb_y0), tb_w, tb_h, fill=True, facecolor="#F8FAFC", edgecolor="#0F172A", linewidth=1.5))
    
    # Grid lines
    ax.plot([tb_x0, tb_x0 + tb_w], [tb_y0 + 8.0, tb_y0 + 8.0], color="#0F172A", lw=1.0)
    ax.plot([tb_x0, tb_x0 + tb_w], [tb_y0 + 4.5, tb_y0 + 4.5], color="#0F172A", lw=0.8)
    ax.plot([tb_x0 + 24.0, tb_x0 + 24.0], [tb_y0, tb_y0 + 8.0], color="#0F172A", lw=0.8)
    ax.plot([tb_x0 + 34.0, tb_x0 + 34.0], [tb_y0, tb_y0 + 4.5], color="#0F172A", lw=0.8)
    
    # Title & Information
    ax.text(tb_x0 + 1.5, tb_y0 + 10.8, "NAVEEN CAD / ADVANCED TURBINE SYSTEMS", fontsize=7.5, weight="bold", color="#1E293B")
    ax.text(tb_x0 + 1.5, tb_y0 + 9.0, f"TITLE: {title}", fontsize=8.5, weight="bold", color="#0F172A")
    
    ax.text(tb_x0 + 1.5, tb_y0 + 6.0, f"DWG NO: {dwg_no}", fontsize=8.0, weight="bold", color="#0369A1")
    ax.text(tb_x0 + 25.5, tb_y0 + 6.0, f"MATERIAL: {material}", fontsize=6.8, weight="bold", color="#334155")
    
    ax.text(tb_x0 + 1.5, tb_y0 + 2.2, f"GEN TOL: {tolerance}", fontsize=6.5, color="#475569")
    ax.text(tb_x0 + 25.5, tb_y0 + 2.2, f"SCALE: {scale}", fontsize=6.5, color="#475569")
    ax.text(tb_x0 + 35.0, tb_y0 + 2.2, f"SHEET: {sheet_no}", fontsize=6.5, weight="bold", color="#0F172A")

def draw_sheet_border(ax):
    """Draws drawing border, zone markers, and first-angle projection symbol."""
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 70)
    ax.axis("off")
    
    # Outer sheet border
    ax.add_patch(patches.Rectangle((1.5, 1.5), 97.0, 67.0, fill=False, edgecolor="#0F172A", linewidth=1.8))
    # Inner border line
    ax.add_patch(patches.Rectangle((2.5, 2.5), 95.0, 65.0, fill=False, edgecolor="#64748B", linewidth=0.6))
    
    # First Angle Projection Symbol at (5, 64)
    px = 6.0
    py = 65.0
    ax.plot([px, px+3.5], [py-0.8, py-1.4], color="#0F172A", lw=0.8)
    ax.plot([px, px+3.5], [py+0.8, py+1.4], color="#0F172A", lw=0.8)
    ax.plot([px, px], [py-0.8, py+0.8], color="#0F172A", lw=0.8)
    ax.plot([px+3.5, px+3.5], [py-1.4, py+1.4], color="#0F172A", lw=0.8)
    circle1 = plt.Circle((px + 5.5, py), 0.8, fill=False, edgecolor="#0F172A", lw=0.8)
    circle2 = plt.Circle((px + 5.5, py), 1.4, fill=False, edgecolor="#0F172A", lw=0.8)
    ax.add_patch(circle1)
    ax.add_patch(circle2)
    ax.text(px + 7.5, py - 0.5, "FIRST ANGLE PROJ", fontsize=6, color="#475569", weight="bold")


# ==============================================================================
# SHEET 1: ROTOR BLADE TOOLING & VARTM MOLD SPLIT DRAWING
# ==============================================================================
fig, ax = plt.subplots(figsize=(16, 11), dpi=300)
draw_sheet_border(ax)
draw_title_block(ax, dwg_no="HAWT-OPT-001", title="NOVEL BIO-AEROELASTIC ROTOR BLADE VARTM TOOLING",
                 sheet_no="1 OF 3", material="GFRP/CFRP HYBRID + EPOXY", tolerance="ISO 2768-cL", scale="1:20")

# Header Label
ax.text(18.0, 65.0, "DESIGN FOR MANUFACTURING (DFM) SPECIFICATION: VARTM SPLIT-MOLD TOOLING", fontsize=10, weight="bold", color="#0F172A")

# --- VIEW 1: BLADE PLANFORM (TOP VIEW) WITH TUBERCLES & SWEPT WINGLET ---
ax.text(5.0, 58.0, "VIEW A: ROTOR BLADE AERODYNAMIC PLANFORM & SPANWISE STATIONS", fontsize=8.5, weight="bold", color="#1E3A8A")

# Span centerline from X=8 to X=85 at Y=46
span_x = np.linspace(8.0, 84.0, 300)
# Chord distribution and LE/TE curves
chord_w = 4.5 * np.exp(-0.02 * (span_x - 8.0)) + 1.2
# Add 4 tubercle cycles between X=25 and X=55
tubercle_mod = np.where((span_x >= 25.0) & (span_x <= 55.0), 0.65 * np.sin(2.0 * np.pi * (span_x - 25.0) / 7.5), 0.0)
# Aft sweep tip past X=68
sweep_offset = np.where(span_x > 68.0, -0.015 * ((span_x - 68.0) ** 2), 0.0)

le_y = 46.0 + (0.35 * chord_w) + tubercle_mod + sweep_offset
te_y = 46.0 - (0.65 * chord_w) + sweep_offset

# Fill Blade
blade_poly = list(zip(span_x, le_y)) + list(zip(reversed(span_x), reversed(te_y)))
ax.add_patch(Polygon(blade_poly, closed=True, facecolor="#F1F5F9", edgecolor="#0284C7", lw=1.5))

# Draw Internal Box Spar Webs (Hollow Spar)
spar_le = 46.0 + (0.12 * chord_w) + (0.5 * tubercle_mod) + sweep_offset
spar_te = 46.0 - (0.22 * chord_w) + sweep_offset
ax.plot(span_x[20:250], spar_le[20:250], color="#DC2626", ls="--", lw=1.2, label="Internal Spar Cap / Shear Web (UD Carbon)")
ax.plot(span_x[20:250], spar_te[20:250], color="#DC2626", ls="--", lw=1.2)

# Root Circular Flange detail
ax.add_patch(patches.Rectangle((6.0, 43.0), 2.5, 6.0, facecolor="#E2E8F0", edgecolor="#0F172A", lw=1.2))
ax.text(5.5, 40.5, "Root Flange\nPCD Dia 180", fontsize=6.5, color="#0F172A", weight="bold")

# Station Callout Markers
stations = [(8.0, "R340 (Root)"), (28.0, "Crest 1"), (35.5, "Crest 2"), (43.0, "Crest 3"), (50.5, "Crest 4"), (68.0, "Sweep Start"), (84.0, "R4500 (Tip)")]
for sx, sname in stations:
    ax.plot([sx, sx], [46.0 - 5.5, 46.0 + 5.5], color="#94A3B8", ls=":", lw=0.8)
    ax.text(sx - 1.5, 52.5, sname, fontsize=6.0, rotation=35, color="#475569")

# Dimensions & Annotations on Planform
ax.annotate("", xy=(84.0, 39.0), xytext=(8.0, 39.0), arrowprops=dict(arrowstyle="<->", color="#0F172A", lw=1.0))
ax.text(42.0, 37.5, "ROTOR SPAN L = 4160 mm (RADIUS R = 4500 mm)", fontsize=7.5, weight="bold", color="#0F172A")

# --- VIEW 2: SECTION A-A (VARTM SPLIT TOOLING & DEMOLD DRAFT) ---
ax.text(5.0, 33.0, "SECTION A-A: VARTM TOOLING SPLIT LINE & SHEAR WEB BONDING", fontsize=8.0, weight="bold", color="#1E3A8A")

# Airfoil Cross Section at X=18, Y=22
cx = 18.0
cy = 23.0
# NACA 4412 like shape
theta = np.linspace(0, 2*np.pi, 100)
x_af = cx + 8.0 * (np.cos(theta) - 1.0) * -0.5
y_af = cy + 2.2 * np.sin(theta) * (1.0 - (x_af - cx) / 8.0)

ax.plot(x_af, y_af, color="#0284C7", lw=1.8)
# Mold Upper & Lower Shell parting line
ax.plot([cx - 1.0, cx + 9.5], [cy, cy], color="#D97706", ls="-.", lw=1.2)
ax.text(cx + 10.0, cy - 0.3, "Tooling Split Line (Chordwise)", fontsize=6.5, color="#D97706", weight="bold")

# Internal shear webs
ax.plot([cx + 3.0, cx + 3.0], [cy - 1.4, cy + 1.4], color="#DC2626", lw=2.0)
ax.plot([cx + 5.5, cx + 5.5], [cy - 1.1, cy + 1.1], color="#DC2626", lw=2.0)
ax.text(cx + 2.0, cy - 3.2, "Box Spar Shear Webs\nBondline 4.0 ± 0.5 mm", fontsize=6.0, color="#DC2626", weight="bold")

# Tooling Demold Draft Angle Callout
ax.text(cx - 2.0, cy + 3.5, "Demold Draft Angle: 2.5° Min", fontsize=6.5, weight="bold", color="#047857")

# --- VIEW 3: SECTION B-B (CIRCULAR ROOT T-BOLT INSERT PATTERN) ---
ax.text(50.0, 33.0, "SECTION B-B: BLADE ROOT T-BOLT STEEL BUSHING CIRCLE", fontsize=8.0, weight="bold", color="#1E3A8A")
rx = 64.0
ry = 22.0
circle_root = plt.Circle((rx, ry), 5.5, fill=True, facecolor="#F8FAFC", edgecolor="#0F172A", lw=1.5)
circle_pcd = plt.Circle((rx, ry), 4.3, fill=False, edgecolor="#DC2626", ls="--", lw=1.0)
circle_bore = plt.Circle((rx, ry), 2.5, fill=True, facecolor="#FFFFFF", edgecolor="#0F172A", lw=1.2)
ax.add_patch(circle_root)
ax.add_patch(circle_pcd)
ax.add_patch(circle_bore)

# 12 T-bolt Bushings on PCD
for i in range(12):
    ang = 2.0 * np.pi * i / 12
    bx = rx + 4.3 * np.cos(ang)
    by = ry + 4.3 * np.sin(ang)
    t_hole = plt.Circle((bx, by), 0.35, fill=True, facecolor="#0284C7", edgecolor="#0F172A", lw=0.6)
    ax.add_patch(t_hole)

ax.text(rx - 4.5, ry - 7.2, "12x M16 Cross T-Bolt Inserts\nPCD Dia 180 mm | Equispaced 30°", fontsize=6.8, weight="bold", color="#0F172A")

# --- GD&T FEATURE CONTROL FRAMES ---
# Aerodynamic Profile Surface GD&T
gdt_x = 5.0
# Aerodynamic Profile Surface GD&T
gdt_x = 5.0
gdt_y = 7.0
ax.add_patch(patches.Rectangle((gdt_x, gdt_y), 18.0, 4.0, fill=True, facecolor="#FFFFFF", edgecolor="#0F172A", lw=1.0))
ax.plot([gdt_x + 4.0, gdt_x + 4.0], [gdt_y, gdt_y + 4.0], color="#0F172A", lw=0.8)
ax.plot([gdt_x + 10.0, gdt_x + 10.0], [gdt_y, gdt_y + 4.0], color="#0F172A", lw=0.8)
# Vector Arc for profile symbol
arc_patch = Arc((gdt_x + 2.0, gdt_y + 1.2), 2.2, 2.0, angle=0, theta1=0, theta2=180, edgecolor="#0F172A", lw=1.5)
ax.add_patch(arc_patch)
ax.text(gdt_x + 5.0, gdt_y + 1.3, "1.5", fontsize=8.0, weight="bold")
ax.text(gdt_x + 11.0, gdt_y + 1.3, "A | B", fontsize=8.0, weight="bold")
ax.text(gdt_x, gdt_y + 4.5, "AERO PROFILE TOLERANCE (ISO 1101)", fontsize=6.5, weight="bold", color="#1E293B")

# True Position GD&T on T-Bolts
pos_x = 26.0
pos_y = 7.0
ax.add_patch(patches.Rectangle((pos_x, pos_y), 20.0, 4.0, fill=True, facecolor="#FFFFFF", edgecolor="#0F172A", lw=1.0))
ax.plot([pos_x + 4.0, pos_x + 4.0], [pos_y, pos_y + 4.0], color="#0F172A", lw=0.8)
ax.plot([pos_x + 13.0, pos_x + 13.0], [pos_y, pos_y + 4.0], color="#0F172A", lw=0.8)
# Vector crosshair circle for true position
pos_circ = plt.Circle((pos_x + 2.0, pos_y + 2.0), 1.0, fill=False, edgecolor="#0F172A", lw=1.2)
ax.add_patch(pos_circ)
ax.plot([pos_x + 0.6, pos_x + 3.4], [pos_y + 2.0, pos_y + 2.0], color="#0F172A", lw=0.9)
ax.plot([pos_x + 2.0, pos_x + 2.0], [pos_y + 0.6, pos_y + 3.4], color="#0F172A", lw=0.9)
ax.text(pos_x + 4.8, pos_y + 1.3, "Dia 0.4 (M)", fontsize=7.5, weight="bold")
ax.text(pos_x + 14.5, pos_y + 1.3, "A", fontsize=8.0, weight="bold")
ax.text(pos_x, pos_y + 4.5, "ROOT T-BOLT TRUE POSITION (MMC)", fontsize=6.5, weight="bold", color="#1E293B")

plt.tight_layout()
fig1_path = "reports/portfolio_figures/fig7_dfm_blade_tooling_drawing.png"
fig.savefig(fig1_path, dpi=300)
plt.close(fig)
print(f"  [Sheet 1] Generated: {fig1_path} ({os.path.getsize(fig1_path):,} bytes)")


# ==============================================================================
# SHEET 2: MAIN ROTOR SHAFT CNC MACHINING & GRINDING DRAWING
# ==============================================================================
fig, ax = plt.subplots(figsize=(16, 11), dpi=300)
draw_sheet_border(ax)
draw_title_block(ax, dwg_no="HAWT-OPT-002", title="PRECISION CNC MACHINED HOLLOW MAIN SHAFT",
                 sheet_no="2 OF 3", material="42CrMo4+QT (850 MPa)", tolerance="ISO 2768-mK", scale="1:5")

ax.text(18.0, 65.0, "DESIGN FOR MANUFACTURING (DFM) SPECIFICATION: CNC TURNING & PRECISION GRINDING", fontsize=10, weight="bold", color="#0F172A")

# --- VIEW 1: FULL CROSS-SECTION / ELEVATION VIEW OF STEPPED SHAFT ---
ax.text(5.0, 58.0, "VIEW A: LONGITUDINAL SECTION WITH TOLERANCED BEARING JOURNALS & RELIEFS", fontsize=8.5, weight="bold", color="#1E3A8A")

# Shaft centerline from X=8 to X=88 at Y=40
ax.plot([6.0, 90.0], [40.0, 40.0], color="#D97706", ls="-.", lw=1.2, label="Shaft Centerline Axis A-B")

# Shaft geometry stations along X:
# Flange: X=8 to X=12, Y=40-10 to 40+10 (Dia 210)
# Front Journal: X=12 to X=32, Y=40-5.0 to 40+5.0 (Dia 80 m6)
# Intermediate Step: X=32 to X=50, Y=40-4.8 to 40+4.8 (Dia 78)
# Rear Journal: X=50 to X=65, Y=40-4.5 to 40+4.5 (Dia 75 k6)
# Generator Drive Seat: X=65 to X=86, Y=40-4.0 to 40+4.0 (Dia 70 h6)
# Through Bore: Y=40-2.0 to 40+2.0 (Dia 38)

# Upper Shaft Half
sh_upper = [
    (8.0, 40.0), (8.0, 50.0), (12.0, 50.0), # Flange
    (12.0, 45.0), (32.0, 45.0),              # Front Journal
    (32.0, 44.8), (50.0, 44.8),              # Inter Span
    (50.0, 44.5), (65.0, 44.5),              # Rear Journal
    (65.0, 44.0), (86.0, 44.0),              # Gen Drive
    (86.0, 42.0), (8.0, 42.0)                # Bore & back to origin
]

# Lower Shaft Half (mirrored)
sh_lower = [
    (8.0, 40.0), (8.0, 30.0), (12.0, 30.0), # Flange
    (12.0, 35.0), (32.0, 35.0),              # Front Journal
    (32.0, 35.2), (50.0, 35.2),              # Inter Span
    (50.0, 35.5), (65.0, 35.5),              # Rear Journal
    (65.0, 36.0), (86.0, 36.0),              # Gen Drive
    (86.0, 38.0), (8.0, 38.0)                # Bore
]

ax.add_patch(Polygon(sh_upper, closed=True, facecolor="#F1F5F9", edgecolor="#0F172A", lw=1.6))
ax.add_patch(Polygon(sh_lower, closed=True, facecolor="#F1F5F9", edgecolor="#0F172A", lw=1.6))

# Crosshatch section for steel body
ax.plot([8.0, 86.0], [42.0, 42.0], color="#0284C7", lw=1.2)
ax.plot([8.0, 86.0], [38.0, 38.0], color="#0284C7", lw=1.2)
ax.text(45.0, 39.5, "⌀ 38 mm CENTRAL CABLE CONDUIT BORE", fontsize=6.8, color="#0369A1", weight="bold")

# DIN 509 Form F Grinding Undercuts markers
ax.plot([12.0, 12.0], [44.7, 45.3], color="#DC2626", lw=2.5)
ax.plot([50.0, 50.0], [44.2, 44.8], color="#DC2626", lw=2.5)
ax.annotate("DIN 509 - F 1.2 x 0.3\nGrinding Undercut", xy=(12.0, 45.0), xytext=(14.0, 53.0),
            arrowprops=dict(arrowstyle="->", color="#DC2626", lw=1.0), fontsize=6.5, weight="bold", color="#DC2626")
ax.annotate("DIN 509 - F 1.2 x 0.3", xy=(50.0, 44.5), xytext=(51.0, 51.0),
            arrowprops=dict(arrowstyle="->", color="#DC2626", lw=1.0), fontsize=6.5, weight="bold", color="#DC2626")

# DIN 6885 Form A Keyway
ax.add_patch(patches.Rectangle((70.0, 43.0), 12.0, 1.0, facecolor="#FFFFFF", edgecolor="#DC2626", lw=1.2))
ax.text(71.0, 46.5, "DIN 6885-A 20x12x100\nKeyway for PMG Rotor", fontsize=6.5, color="#DC2626", weight="bold")

# Bearing Fits Callout
ax.text(18.0, 47.0, "⌀ 80 m6 (+0.021/+0.009)\nRa 0.8 μm [Front Brg]", fontsize=7.2, weight="bold", color="#047857")
ax.text(53.0, 47.0, "⌀ 75 k6 (+0.018/+0.002)\nRa 0.8 μm [Rear Brg]", fontsize=7.2, weight="bold", color="#047857")
ax.text(71.0, 34.0, "⌀ 70 h6 (0/-0.019)\nRa 1.6 μm [Generator]", fontsize=7.2, weight="bold", color="#0F172A")

# Datum Identifiers [A] and [B]
# Datum A at Front Journal
ax.add_patch(patches.Rectangle((20.0, 33.0), 4.0, 3.0, facecolor="#0F172A", edgecolor="#0F172A"))
ax.text(21.2, 33.8, "A", fontsize=9.0, weight="bold", color="#FFFFFF")
# Datum B at Rear Journal
ax.add_patch(patches.Rectangle((56.0, 33.0), 4.0, 3.0, facecolor="#0F172A", edgecolor="#0F172A"))
ax.text(57.2, 33.8, "B", fontsize=9.0, weight="bold", color="#FFFFFF")

# Overall Length Dimension
ax.annotate("", xy=(86.0, 26.0), xytext=(8.0, 26.0), arrowprops=dict(arrowstyle="<->", color="#0F172A", lw=1.0))
ax.text(42.0, 24.5, "TOTAL SHAFT LENGTH L = 930 mm (FLANGE TO END)", fontsize=7.5, weight="bold", color="#0F172A")

# --- GD&T FEATURE CONTROL FRAMES ---
# Total Runout GD&T
g1_x = 5.0
g1_y = 10.0
ax.add_patch(patches.Rectangle((g1_x, g1_y), 22.0, 4.0, fill=True, facecolor="#FFFFFF", edgecolor="#0F172A", lw=1.0))
ax.plot([g1_x + 4.5, g1_x + 4.5], [g1_y, g1_y + 4.0], color="#0F172A", lw=0.8)
ax.plot([g1_x + 13.0, g1_x + 13.0], [g1_y, g1_y + 4.0], color="#0F172A", lw=0.8)
# Double diagonal arrows for total runout
ax.annotate("", xy=(g1_x + 3.2, g1_y + 3.0), xytext=(g1_x + 1.2, g1_y + 1.0), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.2))
ax.annotate("", xy=(g1_x + 3.8, g1_y + 3.0), xytext=(g1_x + 1.8, g1_y + 1.0), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.2))
ax.text(g1_x + 5.5, g1_y + 1.3, "0.015", fontsize=8.0, weight="bold")
ax.text(g1_x + 14.5, g1_y + 1.3, "A - B", fontsize=8.0, weight="bold")
ax.text(g1_x, g1_y + 4.5, "TOTAL RADIAL RUNOUT (ISO 1101)", fontsize=6.5, weight="bold", color="#1E293B")

# Cylindricity GD&T
g2_x = 30.0
g2_y = 10.0
ax.add_patch(patches.Rectangle((g2_x, g2_y), 15.0, 4.0, fill=True, facecolor="#FFFFFF", edgecolor="#0F172A", lw=1.0))
ax.plot([g2_x + 4.5, g2_x + 4.5], [g2_y, g2_y + 4.0], color="#0F172A", lw=0.8)
# Vector circle with two parallel tangents for cylindricity
ax.add_patch(plt.Circle((g2_x + 2.2, g2_y + 2.0), 0.9, fill=False, edgecolor="#0F172A", lw=1.1))
ax.plot([g2_x + 0.8, g2_x + 2.0], [g2_y + 0.7, g2_y + 3.3], color="#0F172A", lw=1.0)
ax.plot([g2_x + 2.4, g2_x + 3.6], [g2_y + 0.7, g2_y + 3.3], color="#0F172A", lw=1.0)
ax.text(g2_x + 6.0, g2_y + 1.3, "0.008", fontsize=8.0, weight="bold")
ax.text(g2_x, g2_y + 4.5, "CYLINDRICITY ON BEARING SEATS", fontsize=6.5, weight="bold", color="#1E293B")

plt.tight_layout()
fig2_path = "reports/portfolio_figures/fig8_dfm_shaft_machining_drawing.png"
fig.savefig(fig2_path, dpi=300)
plt.close(fig)
print(f"  [Sheet 2] Generated: {fig2_path} ({os.path.getsize(fig2_path):,} bytes)")


# ==============================================================================
# SHEET 3: 15 m SEGMENTED TOWER FABRICATION & WELDMENT DRAWING
# ==============================================================================
fig, ax = plt.subplots(figsize=(16, 11), dpi=300)
draw_sheet_border(ax)
draw_title_block(ax, dwg_no="HAWT-OPT-003", title="15m MODULAR SEGMENTED TOWER & FLANGES",
                 sheet_no="3 OF 3", material="S355JR (EN 10025-2)", tolerance="EN 1090-2 EXC3", scale="1:40")

ax.text(18.0, 65.0, "DESIGN FOR MANUFACTURING (DFM) SPECIFICATION: 3-CAN MODULAR TRANSPORT & WELDMENT", fontsize=10, weight="bold", color="#0F172A")

# --- VIEW 1: FULL 15m TOWER ELEVATION (HORIZONTAL LAYOUT) ---
ax.text(5.0, 58.0, "VIEW A: 3-CAN MODULAR SEGMENTS BREAKDOWN (HIGHWAY TRANSPORT COMPLIANT)", fontsize=8.5, weight="bold", color="#1E3A8A")

# Tower laid horizontally: Base at X=8, Top at X=86. Centerline Y=42
ax.plot([6.0, 88.0], [42.0, 42.0], color="#D97706", ls="-.", lw=1.2)

# Can 1 (Base Can): X=8 to 34 (L=5000 mm, taper Dia 800 to 683.3) -> R=4.0 to 3.42
c1_poly = [(8.0, 42.0+4.0), (34.0, 42.0+3.42), (34.0, 42.0-3.42), (8.0, 42.0-4.0)]
ax.add_patch(Polygon(c1_poly, closed=True, facecolor="#F1F5F9", edgecolor="#0F172A", lw=1.5))
ax.text(17.0, 43.5, "CAN 1 (BASE)\nL = 5.0 m | 760 kg", fontsize=7.0, weight="bold", color="#0F172A")

# Can 2 (Mid Can): X=34 to 60 (L=5000 mm, taper Dia 683.3 to 566.7) -> R=3.42 to 2.83
c2_poly = [(34.0, 42.0+3.42), (60.0, 42.0+2.83), (60.0, 42.0-2.83), (34.0, 42.0-3.42)]
ax.add_patch(Polygon(c2_poly, closed=True, facecolor="#F8FAFC", edgecolor="#0F172A", lw=1.5))
ax.text(43.0, 43.5, "CAN 2 (MID)\nL = 5.0 m | 685 kg", fontsize=7.0, weight="bold", color="#0F172A")

# Can 3 (Top Can): X=60 to 86 (L=5000 mm, taper Dia 566.7 to 450) -> R=2.83 to 2.25
c3_poly = [(60.0, 42.0+2.83), (86.0, 42.0+2.25), (86.0, 42.0-2.25), (60.0, 42.0-2.83)]
ax.add_patch(Polygon(c3_poly, closed=True, facecolor="#F1F5F9", edgecolor="#0F172A", lw=1.5))
ax.text(69.0, 43.5, "CAN 3 (TOP)\nL = 5.0 m | 579 kg", fontsize=7.0, weight="bold", color="#0F172A")

# Flanges
# Base Flange at X=8 (Dia 1000 x 35)
ax.add_patch(patches.Rectangle((7.0, 42.0-5.0), 1.0, 10.0, facecolor="#0F172A", edgecolor="#0F172A"))
# Field Flange Joint 1 at X=34
ax.plot([34.0, 34.0], [42.0-3.8, 42.0+3.8], color="#DC2626", lw=2.5)
ax.annotate("Field Joint 1 (Z=5m)\nInternal L-Flange 24x M24 10.9", xy=(34.0, 45.8), xytext=(28.0, 52.0),
            arrowprops=dict(arrowstyle="->", color="#DC2626", lw=1.0), fontsize=6.5, weight="bold", color="#DC2626")

# Field Flange Joint 2 at X=60
ax.plot([60.0, 60.0], [42.0-3.2, 42.0+3.2], color="#DC2626", lw=2.5)
ax.annotate("Field Joint 2 (Z=10m)\nInternal L-Flange 24x M24 10.9", xy=(60.0, 45.2), xytext=(54.0, 52.0),
            arrowprops=dict(arrowstyle="->", color="#DC2626", lw=1.0), fontsize=6.5, weight="bold", color="#DC2626")

# Top Yaw Flange at X=86
ax.add_patch(patches.Rectangle((86.0, 42.0-2.8), 0.8, 5.6, facecolor="#0F172A", edgecolor="#0F172A"))
ax.text(87.5, 41.5, "Top Yaw Flange\nDia 560 x 30", fontsize=6.5, weight="bold", color="#0F172A")

# Overall Tower Height Dimension
ax.annotate("", xy=(86.0, 32.0), xytext=(8.0, 32.0), arrowprops=dict(arrowstyle="<->", color="#0F172A", lw=1.0))
ax.text(38.0, 30.5, "TOTAL TOWER HEIGHT H = 15,000 mm (15.0 m)", fontsize=7.5, weight="bold", color="#0F172A")

# --- VIEW 2: DETAIL B (SAW WELD BEVEL PREP PER ISO 9692-1) ---
ax.text(5.0, 24.0, "DETAIL B: CIRCUMFERENTIAL SUBMERGED ARC WELD (SAW) PREPARATION", fontsize=7.5, weight="bold", color="#1E3A8A")
wx = 18.0
wy = 15.0
# Bevel joint profile
ax.plot([wx - 6.0, wx - 1.0, wx - 1.0, wx - 6.0], [wy + 3.0, wy + 3.0, wy, wy], color="#0F172A", lw=1.5)
ax.plot([wx + 6.0, wx + 1.0, wx + 1.0, wx + 6.0], [wy + 3.0, wy + 3.0, wy, wy], color="#0F172A", lw=1.5)
# Weld V-groove
ax.plot([wx - 1.0, wx - 0.3], [wy + 3.0, wy + 0.8], color="#DC2626", lw=1.5)
ax.plot([wx + 1.0, wx + 0.3], [wy + 3.0, wy + 0.8], color="#DC2626", lw=1.5)
ax.plot([wx - 0.3, wx + 0.3], [wy + 0.8, wy + 0.8], color="#DC2626", lw=1.5)
ax.text(wx - 5.0, wy - 2.5, "Single-V Butt Prep (ISO 9692-1)\n60° Angle | 2mm Root Face | 1.5mm Gap", fontsize=6.5, weight="bold", color="#047857")

# --- VIEW 3: DETAIL C (BASE FLANGE 16x M24 FASTENER PATTERN) ---
ax.text(45.0, 24.0, "DETAIL C: BASE FLANGE & M24 ANCHOR CIRCLE (FOUNDATION INTERFACE)", fontsize=7.5, weight="bold", color="#1E3A8A")
fx = 68.0
fy = 14.0
c_outer = plt.Circle((fx, fy), 5.8, fill=True, facecolor="#F8FAFC", edgecolor="#0F172A", lw=1.5)
c_pcd   = plt.Circle((fx, fy), 5.3, fill=False, edgecolor="#DC2626", ls="--", lw=1.0)
c_inner = plt.Circle((fx, fy), 4.5, fill=True, facecolor="#FFFFFF", edgecolor="#0F172A", lw=1.2)
ax.add_patch(c_outer)
ax.add_patch(c_pcd)
ax.add_patch(c_inner)

for i in range(16):
    ang = 2.0 * np.pi * i / 16
    bx = fx + 5.3 * np.cos(ang)
    by = fy + 5.3 * np.sin(ang)
    b_hole = plt.Circle((bx, by), 0.28, fill=True, facecolor="#0284C7", edgecolor="#0F172A", lw=0.6)
    ax.add_patch(b_hole)

ax.text(fx - 7.5, fy - 7.5, "16x Dia 26 mm Holes on PCD 920 mm\nFor M24 Gr 8.8 Helical Anchor Studs", fontsize=6.8, weight="bold", color="#0F172A")

# Flatness GD&T
f_x = 5.0
f_y = 5.0
ax.add_patch(patches.Rectangle((f_x, f_y), 15.0, 4.0, fill=True, facecolor="#FFFFFF", edgecolor="#0F172A", lw=1.0))
ax.plot([f_x + 4.5, f_x + 4.5], [f_y, f_y + 4.0], color="#0F172A", lw=0.8)
# Vector parallelogram for flatness
flat_poly = [(f_x + 1.2, f_y + 1.2), (f_x + 3.2, f_y + 1.2), (f_x + 3.8, f_y + 2.8), (f_x + 1.8, f_y + 2.8)]
ax.add_patch(Polygon(flat_poly, closed=True, fill=False, edgecolor="#0F172A", lw=1.2))
ax.text(f_x + 6.0, f_y + 1.3, "0.3", fontsize=8.0, weight="bold")
ax.text(f_x, f_y + 4.5, "FLANGE CONTACT FLATNESS (ISO 1101)", fontsize=6.5, weight="bold", color="#1E293B")

plt.tight_layout()
fig3_path = "reports/portfolio_figures/fig9_dfm_tower_fabrication_drawing.png"
fig.savefig(fig3_path, dpi=300)
plt.close(fig)
print(f"  [Sheet 3] Generated: {fig3_path} ({os.path.getsize(fig3_path):,} bytes)")

print("\nSUCCESS: All 3 2D Manufacturing Drawing Sheets Generated!")
