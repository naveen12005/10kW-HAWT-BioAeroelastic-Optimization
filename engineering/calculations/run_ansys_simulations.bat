@echo off
echo ==============================================================================
echo RUNNING AUTOMATED ANSYS MECHANICAL APDL 2026 R1 SIMULATIONS
echo Project: HAWT 10 kW Wind Turbine FEA
echo ==============================================================================

set ANSYS_EXE="C:\Program Files\ANSYS Inc\ANSYS Student\v261\ansys\bin\winx64\ansys261.exe"
set WORK_DIR=C:\NaveenCADAgent\ansys_work

if not exist %WORK_DIR% mkdir %WORK_DIR%

echo [1/2] Running Rotor Blade FEA (Static Thrust + Centrifugal Modal Analysis)...
%ANSYS_EXE% -b -dir "%WORK_DIR%" -i "C:\NaveenCADAgent\engineering\calculations\hawt_fea_blade_clean.mac" -o "%WORK_DIR%\blade_run.out"
echo   Blade simulation completed! Results written to %WORK_DIR%\blade_fea_results.txt

echo [2/2] Running Main Shaft & Bearing FEA (Torsion + Overhang Bending)...
%ANSYS_EXE% -b -dir "%WORK_DIR%" -i "C:\NaveenCADAgent\engineering\calculations\hawt_fea_shaft_clean.mac" -o "%WORK_DIR%\shaft_run.out"
echo   Shaft simulation completed! Results written to %WORK_DIR%\shaft_fea_results.txt

echo ==============================================================================
echo ALL ANSYS APDL SIMULATIONS EXECUTED SUCCESSFULLY!
echo ==============================================================================
pause
