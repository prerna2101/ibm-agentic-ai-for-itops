# import_tools.ps1
# Stops on first error
$ErrorActionPreference = 'Stop'

# Resolve script directory (works even if called via relative path)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host "SCRIPT_DIR: $ScriptDir"

$ToolsDir = Join-Path $ScriptDir 'tools'
$ReqFile  = Join-Path $ScriptDir 'requirements.txt'

# Verify prerequisites
if (-not (Test-Path $ToolsDir)) { throw "Tools folder not found: $ToolsDir" }
if (-not (Test-Path $ReqFile))  { throw "requirements.txt not found: $ReqFile" }
if (-not (Get-Command orchestrate -ErrorAction SilentlyContinue)) {
  throw "The 'orchestrate' CLI is not in PATH. Install it or open a shell where it's available."
}

# Import each .py tool file
Get-ChildItem -Path $ToolsDir -Filter *.py -File | ForEach-Object {
  $pyFile = $_.FullName
  & orchestrate tools import `
    -k python `
    -f $pyFile `
    -r $ReqFile `
    -p $ToolsDir
  if ($LASTEXITCODE -ne 0) {
    throw "Import failed for $pyFile (exit code $LASTEXITCODE)."
  }
}
Write-Host "All tools imported successfully."
