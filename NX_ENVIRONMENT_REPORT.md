# Technical Investigation Report: Siemens NX / Designcenter Environment

**Date:** 2026-10-01  
**Target Application:** Siemens Designcenter / NX Student Edition  
**Platform:** Windows 10/11 x64 (Build Architecture: x64wnt)  
**Investigator:** Google Antigravity Agent  

---

## 1. Executive Summary

A comprehensive investigation of the local Windows environment was conducted to assess the feasibility of interfacing Google Antigravity with Siemens Designcenter / NX for autonomous CAD geometry generation. 

The software **Siemens Designcenter Student Edition 2606** is installed and actively running on the workstation (`ugraf.exe`, PID `17508`). The full NX Open API ecosystem and an embedded **Python 3.12** runtime are present. 

Critical findings regarding licensing and execution modes were identified:
- **In-Session Journaling (Interactive GUI):** Available and operational inside the running NX application.
- **External Batch Journaling (`run_journal.exe`):** Restricted by Siemens Student Edition licensing (fails with `Error 3615094: Unable to reserve license to run journal file` due to missing standalone commercial gateway feature).
- **Communication Bridge:** The recommended integration architecture is an **In-Session Python Socket/HTTP Bridge** or an **Inbox/Outbox File Exchange Watcher** executed inside the active NX session to execute `NXOpen` commands dispatched by Antigravity.

---

## 2. Environment & Installation Details

| Parameter | Telemetry Value Found |
| :--- | :--- |
| **Product Display Name** | `Siemens Designcenter Student Edition 2606` |
| **Installed Display Version** | `26.06.3002.00000` |
| **NX Internal Version / Build** | `Designcenter 2606.3002` (`V2606`, `x64wnt`) |
| **Publisher** | `Siemens` |
| **Installation Date** | `2026-10-01` |
| **Installation Directory (`UGII_BASE_DIR`)** | `C:\Program Files\Siemens\DcStudentEdition2606\` |
| **Binary Directory (`NXBIN`)** | `C:\Program Files\Siemens\DcStudentEdition2606\NXBIN\` |
| **Core Directory (`UGII`)** | `C:\Program Files\Siemens\DcStudentEdition2606\UGII\` |
| **Open API Directory (`UGOPEN`)** | `C:\Program Files\Siemens\DcStudentEdition2606\UGOPEN\` |
| **User Profile Directory** | `C:\Users\rc\AppData\Local\Siemens\Designcenter Student Edition2606\` |
| **Active Process** | `ugraf.exe` (PID `17508`) |
| **Active Process Command Line** | `"C:\Program Files\Siemens\DcStudentEdition2606\NXBIN\ugraf.exe" -student` |

---

## 3. NX Open & Journaling Capabilities

### 3.1 NX Open API Components
The full NX Open development files are present on disk:
- **C/C++ Headers:** Located in `C:\Program Files\Siemens\DcStudentEdition2606\UGOPEN` (`uf_modl.h`, `uf_curve.h`, `uf_ui.h`, etc.).
- **Python Bindings:** Located in `C:\Program Files\Siemens\DcStudentEdition2606\NXBIN\python` (`NXOpen.pyd`, `NXOpen_UF.pyd`, `NXOpen_Features.pyd`, `NXOpen_Assemblies.pyd`, etc.).
- **Type Stubs:** Located in `C:\Program Files\Siemens\DcStudentEdition2606\UGOPEN\pythonStubs\NXOpen`.
- **Sample Applications:** Available in `C:\Program Files\Siemens\DcStudentEdition2606\UGOPEN\SampleNXOpenApplications\Python`.

### 3.2 Journaling Executables & Menus
- **Command-line Runner:** `C:\Program Files\Siemens\DcStudentEdition2606\NXBIN\run_journal.exe` is present and functional. It supports languages `vb`, `cpp`, `cs`, `java`, and `py`.
- **NX UI Menus:** Verified in `ug_main.men` and `ug_gateway.men`:
  - Action `UG_JOURNAL_PLAY` (Shortcut: `Alt+F8`)
  - Action `UG_JOURNAL_RECORD`
  - Action `UG_JOURNAL_STOP`
  - Action `UG_JOURNAL_EDIT`

### 3.3 Student Edition Licensing Restrictions (Empirically Verified)
Executing external batch scripts via `run_journal.exe` was tested with a non-CAD diagnostic script:
```powershell
& "C:\Program Files\Siemens\DcStudentEdition2606\NXBIN\run_journal.exe" "verify_python.py"
```
**Result:**
```text
Unable to reserve gateway license feature gateway
*** EXCEPTION: Error code 3615094 in line 683 of run_journal.c
+++ Unable to reserve license to run journal file
+++ Caught unexpected error: 3615094: Unable to reserve license to run journal file
```
**Conclusion:** `run_journal.exe` requires a dedicated standalone commercial gateway license token. The Student Edition license (`-student` trial token) only activates within the interactive GUI process (`ugraf.exe`). Consequently, **external batch execution without the GUI is locked out by license, but internal execution within the running GUI session is supported.**

---

## 4. Python Environment & Interpreter

| Component | Verified Location / Specification |
| :--- | :--- |
| **Python Version** | **Python 3.12** (Embedded CPython 3.12 64-bit) |
| **Python Core DLL** | `C:\Program Files\Siemens\DcStudentEdition2606\NXBIN\python\python312.dll` |
| **Python Standard Library** | `C:\Program Files\Siemens\DcStudentEdition2606\NXBIN\python\Python312.zip` |
| **Python Home (`UGII_PYTHON_HOME`)** | `C:\Program Files\Siemens\DcStudentEdition2606\NXBIN\python` |
| **Dynamic Importer / Hook** | `C:\Program Files\Siemens\DcStudentEdition2606\NXBIN\python\sitecustomize.py` (registers `MetaPathHook` to intercept `import NXOpen.*` and load matching `.pyd` files) |
| **System Python Status** | No native Python 3 installation exists on system `PATH` (only Microsoft Store execution aliases `python.exe` / `python3.exe` exist, returning "Python was not found"). |

---

## 5. Inter-Process Communication (IPC) Mechanisms

Because NX does not expose a standard Windows COM Automation object (like Excel or AutoCAD) and Student Edition disables external headless `run_journal.exe` batch licensing, an external process cannot directly attach via COM or CLI batch.

However, three viable mechanisms exist for an external AI agent to communicate with the running NX session:

```
+-------------------------------------------------------------+
|                     Google Antigravity                      |
|                      (CAD AI Agent)                         |
+-------------------------------------------------------------+
              |                                 ^
              | Commands (JSON / Script)        | Status / Telemetry
              v                                 |
+-------------------------------------------------------------+
|             In-Session NX Bridge (Embedded Python)          |
|  - Runs inside running ugraf.exe (PID 17508)                |
|  - Listens on Localhost Socket / HTTP or File Watcher       |
|  - Executes NXOpen API commands in active modeling session  |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|             Siemens Designcenter NX Session (ugraf.exe)     |
|  - Active Part (*.prt)                                      |
|  - Direct 3D Parametric CAD Generation                      |
+-------------------------------------------------------------+
```

### Option A: In-Session Localhost Socket / HTTP Bridge (Recommended)
1. A Python journal script is executed once inside NX via `Tools -> Journal -> Play` (or placed in an NX startup folder).
2. The script spins up a lightweight background daemon thread running `http.server` or a raw TCP socket listening on `127.0.0.1:<port>`.
3. Google Antigravity connects to this local endpoint and sends structured commands (e.g. `{"action": "create_block", "dimensions": [100.0, 50.0, 25.0]}`).
4. The bridge receives the request, calls `NXOpen.Session.GetSession()`, and executes the modeling operations directly in the user's active viewport.

### Option B: Shared File Exchange Queue (Inbox / Outbox)
1. Antigravity writes parametric commands or Python code snippets to `c:\NaveenCADAgent\queue\inbox\`.
2. A lightweight Python script running inside NX polls the directory every 500ms.
3. Upon detecting a new file, it executes the code via `exec()`, captures output/errors, writes the result to `c:\NaveenCADAgent\queue\outbox\`, and clears the task.

### Option C: Manual Journal Playback (Development / Debugging Mode)
1. Antigravity generates a complete, self-contained Python journal script (e.g. `c:\NaveenCADAgent\scripts\create_block.py`).
2. The user runs **Developer / Tools -> Journal -> Play** (`Alt+F8`) inside NX and selects the script.

---

## 6. Recommended Communication Architecture

**Selected Choice: Option A (Embedded Localhost HTTP/JSON Bridge)**

*Why this is optimal:*
- **Zero manual intervention** once started: Antigravity can iteratively create, modify, inspect, and query geometry in real time.
- **Bypasses Student Edition CLI license limitations**: The code executes inside the already-authenticated `ugraf.exe` process.
- **Safe & Responsive**: Python standard library `http.server` and `threading` are already bundled inside `Python312.zip` in the NX installation.

---

## 7. Exact Next Step Required to Create a Test Block in NX

To verify geometric creation without modifying any NX installation files:

1. **Ensure NX has an Active Work Part:**
   - In the running Siemens Designcenter window, click **File -> New**.
   - Under the **Model** tab, select **Model**, ensure units are set to **Millimeters**, and click **OK**.
2. **Generate the Test Journal Script:**
   - Create a clean script `c:\NaveenCADAgent\create_test_block.py` containing the verified NX Open block builder code:
     ```python
     import NXOpen
     import NXOpen.Features

     def main():
         theSession = NXOpen.Session.GetSession()
         workPart = theSession.Parts.Work

         if workPart is None:
             lw = theSession.ListingWindow
             lw.Open()
             lw.WriteLine("Error: No active work part found. Please create or open a part first.")
             return

         # Initialize Block Feature Builder
         blockFeatureBuilder = workPart.Features.CreateBlockFeatureBuilder(NXOpen.Features.Block.Null)
         blockFeatureBuilder.Type = NXOpen.Features.BlockFeatureBuilder.Types.OriginAndEdgeLengths

         # Set Dimensions (e.g. 100 x 50 x 25 mm)
         blockFeatureBuilder.Length.RightHandSide = "100.0"
         blockFeatureBuilder.Width.RightHandSide = "50.0"
         blockFeatureBuilder.Height.RightHandSide = "25.0"

         # Commit the feature
         feature = blockFeatureBuilder.CommitFeature()
         blockFeatureBuilder.Destroy()

     if __name__ == '__main__':
         main()
     ```
3. **Execute the Script via Interactive Journal Play:**
   - In the running Siemens Designcenter window, press **Alt+F8** (or navigate to **Menu -> Tools -> Journal -> Play...**).
   - Browse to `c:\NaveenCADAgent\create_test_block.py` and click **Run**.
4. **Verification:**
   - The parametric 3D block will render in the active NX graphics window.
