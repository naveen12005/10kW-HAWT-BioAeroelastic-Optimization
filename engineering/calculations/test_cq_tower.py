"""
Test CadQuery assembly construction for HAWT 10 kW Wind Turbine
"""
import cadquery as cq
import math
import time

t0 = time.time()
print("Starting HAWT 10 kW assembly test...")

# 1. Foundation Block
foundation = (
    cq.Workplane("XY")
    .box(3600.0, 3600.0, 800.0)
    .translate((0, 0, -400.0))
)
pedestal = (
    cq.Workplane("XY")
    .cylinder(150.0, 600.0) # height 150, radius 600
    .translate((0, 0, 75.0))
)
foundation = foundation.union(pedestal)
print("Foundation created in", round(time.time() - t0, 2), "s")

# 2. Tower (H = 15000 mm, Base OD 800, Top OD 450)
t_tower_0 = time.time()
tower_shell = (
    cq.Workplane("XY")
    .workplane(offset=150.0)
    .circle(400.0) # Base R = 400
    .workplane(offset=15000.0)
    .circle(225.0) # Top R = 225
    .loft(combine=True)
)
tower_flange_bot = (
    cq.Workplane("XY")
    .cylinder(35.0, 500.0) # radius 500
    .translate((0, 0, 150.0 + 17.5))
)
tower_flange_top = (
    cq.Workplane("XY")
    .cylinder(30.0, 280.0) # radius 280
    .translate((0, 0, 15150.0 - 15.0))
)
tower = tower_shell.union(tower_flange_bot).union(tower_flange_top)
print("Tower created in", round(time.time() - t_tower_0, 2), "s")

print("Total test passed in", round(time.time() - t0, 2), "s")
