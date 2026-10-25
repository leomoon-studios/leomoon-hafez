[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$ArtifactDirectory,
    [Parameter(Mandatory = $true)][ValidatePattern('^\d+\.\d+\.\d+$')][string]$Version,
    [ValidateSet("x64", "arm64")][string]$Architecture = "x64"
)

$ErrorActionPreference = "Stop"
$artifacts = (Resolve-Path -LiteralPath $ArtifactDirectory).Path
$installer = Join-Path $artifacts "leomoon-hafez-$Version-windows-$Architecture-setup.exe"
if (-not (Test-Path -LiteralPath $installer -PathType Leaf)) { throw "Windows installer is missing" }
$testRoot = Join-Path $env:RUNNER_TEMP "leomoon-hafez-windows-installer-smoke"
$installDirectory = Join-Path $testRoot "application"
function Invoke-CheckedProcess([string]$FilePath, [string[]]$Arguments, [int]$TimeoutSeconds = 600) {
    $process = Start-Process -FilePath $FilePath -ArgumentList $Arguments -PassThru
    if (-not $process.WaitForExit($TimeoutSeconds * 1000)) { $process.Kill($true); throw "$FilePath did not finish within $TimeoutSeconds seconds" }
    if ($process.ExitCode -ne 0) { throw "$FilePath failed with exit code $($process.ExitCode)" }
}
try {
    Remove-Item -LiteralPath $testRoot -Recurse -Force -ErrorAction SilentlyContinue
    New-Item -ItemType Directory -Path $testRoot | Out-Null
    $arguments = @("/SP-", "/VERYSILENT", "/SUPPRESSMSGBOXES", "/NORESTART", "/DIR=`"$installDirectory`"")
    Invoke-CheckedProcess $installer $arguments
    $application = Join-Path $installDirectory "LeoMoon Hafez.exe"
    if (-not (Test-Path -LiteralPath $application -PathType Leaf)) { throw "Installed application is missing" }
    if (Get-ChildItem -LiteralPath $installDirectory -Recurse -File -Include msvcp100.dll,msvcr100.dll,istask.dll) { throw "Installer deployed an obsolete binary" }
    $process = Start-Process -FilePath $application -PassThru
    Start-Sleep -Seconds 5
    if ($process.HasExited) { throw "Installed application exited during smoke test" }
    $process.Kill($true)
    Invoke-CheckedProcess $installer $arguments
    $uninstaller = Join-Path $installDirectory "unins000.exe"
    if (-not (Test-Path -LiteralPath $uninstaller -PathType Leaf)) { throw "Windows uninstaller is missing" }
    Invoke-CheckedProcess $uninstaller @("/VERYSILENT", "/SUPPRESSMSGBOXES", "/NORESTART")
    if (Test-Path -LiteralPath $installDirectory) { throw "Application directory remains after uninstall" }
} finally {
    Remove-Item -LiteralPath $testRoot -Recurse -Force -ErrorAction SilentlyContinue
}
Write-Host "Windows installer install, upgrade, launch, and uninstall checks passed"
