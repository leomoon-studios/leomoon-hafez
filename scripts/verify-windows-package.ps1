[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$StageDirectory,
    [Parameter(Mandatory = $true)][string]$InstallerPath,
    [Parameter(Mandatory = $true)][ValidatePattern('^\d+\.\d+\.\d+$')][string]$Version,
    [Parameter(Mandatory = $true)][ValidateSet("x64", "arm64")][string]$Architecture
)

$ErrorActionPreference = "Stop"
$stage = (Resolve-Path -LiteralPath $StageDirectory).Path
$installer = (Resolve-Path -LiteralPath $InstallerPath).Path
$application = Join-Path $stage "LeoMoon Hafez.exe"
if (-not (Test-Path -LiteralPath $application -PathType Leaf)) { throw "The staged application is missing" }
if ((Split-Path -Leaf $installer) -ne "leomoon-hafez-$Version-windows-$Architecture-setup.exe") { throw "Installer filename does not match the requested version and architecture" }
foreach ($forbidden in @("msvcp100.dll", "msvcr100.dll", "istask.dll")) {
    if (Get-ChildItem -LiteralPath $stage -Recurse -File -Filter $forbidden) { throw "Obsolete binary is staged: $forbidden" }
}
$dumpbin = Get-Command dumpbin.exe -ErrorAction SilentlyContinue
if (-not $dumpbin) { throw "dumpbin.exe is required to verify PE dependencies" }
$expectedMachine = if ($Architecture -eq "arm64") { 0xAA64 } else { 0x8664 }
$binaries = Get-ChildItem -LiteralPath $stage -Recurse -File |
    Where-Object { $_.Extension -in ".exe", ".dll", ".pyd" } |
    Where-Object {
        $candidateBytes = [System.IO.File]::ReadAllBytes($_.FullName)
        $candidateBytes.Length -ge 2 -and [System.Text.Encoding]::ASCII.GetString($candidateBytes, 0, 2) -eq "MZ"
    }
foreach ($binary in $binaries) {
    $bytes = [System.IO.File]::ReadAllBytes($binary.FullName)
    $peOffset = [System.BitConverter]::ToInt32($bytes, 0x3c)
    if ([System.BitConverter]::ToUInt16($bytes, $peOffset + 4) -ne $expectedMachine) { throw "$($binary.FullName) has the wrong architecture" }
    $dependencies = & $dumpbin.Source /DEPENDENTS $binary.FullName
    if ($LASTEXITCODE -ne 0) { throw "dumpbin /DEPENDENTS failed for $($binary.FullName)" }
    foreach ($forbidden in @("MSVCP100.DLL", "MSVCR100.DLL")) {
        if ($dependencies -match [regex]::Escape($forbidden)) { throw "$($binary.FullName) imports obsolete runtime $forbidden" }
    }
}
Write-Host "Verified $installer"
