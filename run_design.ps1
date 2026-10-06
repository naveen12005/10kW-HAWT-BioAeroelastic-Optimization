param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Name
)

# Strip directory path or .py extension if provided
$scriptName = [System.IO.Path]::GetFileNameWithoutExtension($Name)

$wslCmd = "cd /mnt/c/NaveenCADAgent && source .venv-wsl/bin/activate && python designs/$scriptName.py"
wsl.exe -e bash -lc $wslCmd
