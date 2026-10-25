[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$ApplicationPath,
    [ValidateSet("x64", "arm64")][string]$Architecture = "x64"
)

$ErrorActionPreference = "Stop"
function Assert-PeArchitecture([string]$Path, [string]$ExpectedArchitecture) {
    $bytes = [System.IO.File]::ReadAllBytes($Path)
    if ($bytes.Length -lt 64 -or [System.Text.Encoding]::ASCII.GetString($bytes, 0, 2) -ne "MZ") { throw "$Path is not a PE executable" }
    $peOffset = [System.BitConverter]::ToInt32($bytes, 0x3c)
    $machine = [System.BitConverter]::ToUInt16($bytes, $peOffset + 4)
    $expectedMachine = if ($ExpectedArchitecture -eq "arm64") { 0xAA64 } else { 0x8664 }
    if ($machine -ne $expectedMachine) { throw "$Path is not $ExpectedArchitecture" }
}
$application = (Resolve-Path -LiteralPath $ApplicationPath).Path
Assert-PeArchitecture $application $Architecture
$dumpbin = Get-Command dumpbin.exe -ErrorAction SilentlyContinue
if (-not $dumpbin) { throw "dumpbin.exe is required to verify PE dependencies" }
$dependencies = & $dumpbin.Source /DEPENDENTS $application
if ($LASTEXITCODE -ne 0) { throw "dumpbin /DEPENDENTS failed" }
foreach ($forbidden in @("MSVCP100.DLL", "MSVCR100.DLL")) {
    if ($dependencies -match [regex]::Escape($forbidden)) { throw "$application imports obsolete runtime $forbidden" }
}
Write-Host "Verified PE architecture and direct dependencies for $application"
