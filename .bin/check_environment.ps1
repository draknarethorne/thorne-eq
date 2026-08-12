#!/usr/bin/env pwsh
<#
.SYNOPSIS
  Thorne-EQ local build environment readiness check.

.DESCRIPTION
  Probes the local Windows machine for everything needed to build and run the
  EQMacEmu/Quarm-lineage server: Git, CMake (>=3.12), Visual Studio 2026 with the
  C++ desktop workload, MariaDB 10.3.x, Strawberry Perl (x64), and Python.

  Read-only. Makes no changes. Prints a readiness table and exits non-zero if any
  required component is missing.

.EXAMPLE
  pwsh -File .bin/check_environment.ps1
#>

[CmdletBinding()]
param(
    [switch]$Json
)

$ErrorActionPreference = 'SilentlyContinue'

function New-Result {
    param($Name, $Required, $Found, $Version, $Detail)
    [pscustomobject]@{
        Component = $Name
        Required  = $Required
        Status    = if ($Found) { 'OK' } elseif ($Required) { 'MISSING' } else { 'OPTIONAL' }
        Version   = $Version
        Detail    = $Detail
    }
}

$results = @()

# --- Git ---
$git = Get-Command git -ErrorAction SilentlyContinue
$results += New-Result 'Git' $true ([bool]$git) (& git --version 2>$null) 'https://git-scm.com/download/win'

# --- CMake (>=3.12) ---
$cmake = Get-Command cmake -ErrorAction SilentlyContinue
$cmakeVer = if ($cmake) { (& cmake --version 2>$null | Select-Object -First 1) } else { $null }
$cmakeOk = $false
if ($cmakeVer -match '(\d+)\.(\d+)') {
    $maj = [int]$Matches[1]; $min = [int]$Matches[2]
    $cmakeOk = ($maj -gt 3) -or ($maj -eq 3 -and $min -ge 12)
}
$results += New-Result 'CMake (>=3.12)' $true $cmakeOk $cmakeVer 'Bundled with VS or https://cmake.org/download/'

# --- Visual Studio 2026 + C++ workload (via vswhere) ---
$vswhere = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"
$vsFound = $false; $vsVersion = $null; $vsDetail = 'Install VS 2026 "Desktop development with C++"'
if (Test-Path $vswhere) {
    $vs = & $vswhere -latest -products * -requires Microsoft.VisualStudio.Workload.NativeDesktop -property displayName 2>$null
    $vsVersion = & $vswhere -latest -products * -requires Microsoft.VisualStudio.Workload.NativeDesktop -property catalog_productDisplayVersion 2>$null
    if ($vs) { $vsFound = $true; $vsDetail = $vs }
}
$results += New-Result 'Visual Studio C++' $true $vsFound $vsVersion $vsDetail

# --- MariaDB service + client ---
$mariaSvc = Get-Service -Name 'MariaDB*' -ErrorAction SilentlyContinue | Select-Object -First 1
$mysqlCli = Get-Command mysql -ErrorAction SilentlyContinue
$mariaVer = if ($mysqlCli) { (& mysql --version 2>$null) } else { $null }
$mariaFound = [bool]$mariaSvc -or [bool]$mysqlCli
$mariaDetail = if ($mariaSvc) { "Service: $($mariaSvc.Name) [$($mariaSvc.Status)]" } else { 'Install MariaDB 10.3.x: https://mariadb.org/download/' }
$results += New-Result 'MariaDB 10.3.x' $true $mariaFound $mariaVer $mariaDetail

# --- Strawberry Perl (x64) ---
$perl = Get-Command perl -ErrorAction SilentlyContinue
$perlVer = if ($perl) { ((& perl -e 'print $^V' 2>$null)) } else { $null }
$results += New-Result 'Perl (Strawberry x64)' $true ([bool]$perl) $perlVer 'https://strawberryperl.com/'

# --- Python (tooling, optional-but-recommended) ---
$py = Get-Command python -ErrorAction SilentlyContinue
$pyVer = if ($py) { (& python --version 2>$null) } else { $null }
$results += New-Result 'Python (tooling)' $false ([bool]$py) $pyVer 'https://www.python.org/downloads/'

if ($Json) {
    $results | ConvertTo-Json -Depth 4
}
else {
    Write-Host ''
    Write-Host '  Thorne-EQ Environment Readiness' -ForegroundColor Cyan
    Write-Host '  ===============================' -ForegroundColor Cyan
    $results | Format-Table -AutoSize Component, Status, Version, Detail
}

$missingRequired = @($results | Where-Object { $_.Required -and $_.Status -eq 'MISSING' })
if ($missingRequired.Count -gt 0) {
    Write-Host ("Missing {0} required component(s). See Detail column above." -f $missingRequired.Count) -ForegroundColor Yellow
    exit 1
}
else {
    Write-Host 'All required components present. You are ready to build.' -ForegroundColor Green
    exit 0
}
