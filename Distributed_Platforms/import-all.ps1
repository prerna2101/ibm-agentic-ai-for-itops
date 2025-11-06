# Requires -Version 5.1

# git lfs install - This line is commented out in the original, so it remains commented here, but Git LFS is generally used directly.
# --- Load Environment Variables ---
$ENV_PATH = ".\tools\.env"

if (Test-Path -Path $ENV_PATH -PathType Leaf) {
    # Read the .env file and set each line as an environment variable
    # Using 'Set-Item' with a dynamic path for environment variables
    Get-Content $ENV_PATH | ForEach-Object {
        $line = $_.Trim()
        
        # Skip empty lines, lines starting with #, or lines containing only whitespace
        if (-not ([string]::IsNullOrWhiteSpace($line)) -and -not $line.StartsWith("#")) {
            $parts = $line.Split('=', 2)
            if ($parts.Count -eq 2) {
                $varName = $parts[0].Trim()
                # Remove surrounding quotes from the value, but keep the value as a string
                $varValue = $parts[1].Trim("`"").Trim() 

                # *** CORRECTED LINE HERE: Use Set-Item to dynamically set the variable ***
                Set-Item -Path "Env:$varName" -Value $varValue
            }
        }
    }
    Write-Host "Loaded environment from $ENV_PATH"
}
else {
    Write-Host "Error: .env file not found at $ENV_PATH" -ForegroundColor Red
    exit 1
}

# --- Template Substitution (envsubst equivalent) ---
# PowerShell does not have a direct built-in equivalent for 'envsubst'.
# This block mimics its behavior: reading the template, expanding environment variables, and writing the output.

$TemplatePath = ".\knowledge_base\concertdb.yaml.template"
$OutputPath = ".\knowledge_base\concertdb.yaml"

if (Test-Path -Path $TemplatePath -PathType Leaf) {
    # Read template content
    $templateContent = Get-Content -Path $TemplatePath -Raw

    # Use the 'env' namespace to substitute variables like $ELASTIC_USER
    # This uses the .NET String.Format approach, assuming $VAR in the template
    # might need to be converted to {0}, {1}, etc., for a direct replacement.
    # For a simple replace of $VAR, we can iterate over environment variables.
    
    # Simple substitution by iterating over environment variables
    $substitutedContent = $templateContent
    Get-ChildItem Env: | ForEach-Object {
        # Check for both $VAR and ${VAR} syntax in the template
        $pattern1 = [regex]::Escape("`$") + [regex]::Escape($_.Name)
        $pattern2 = [regex]::Escape("`${") + [regex]::Escape($_.Name) + [regex]::Escape("}")
        
        $substitutedContent = $substitutedContent -replace $pattern1, $_.Value
        $substitutedContent = $substitutedContent -replace $pattern2, $_.Value
    }

    # Write the resulting file
    $substitutedContent | Out-File -FilePath $OutputPath -Encoding UTF8
    Write-Host "Generated $OutputPath from template."

} else {
    Write-Host "Error: Template file not found at $TemplatePath" -ForegroundColor Red
    exit 1
}


# --- Set SCRIPT_DIR ---
# $PSScriptRoot gets the directory of the currently executing script.
$SCRIPT_DIR = $PSScriptRoot


# --- Import Python Tools ---
$python_tools = @(
    "fetch_alerts.py",
    "build_image.py",
    "scan_image.py",
    "update_deployment_yaml.py",
    "deploy_image.py"
)

foreach ($tool in $python_tools) {
    orchestrate tools import `
        -k python `
        -f (Join-Path -Path $SCRIPT_DIR -ChildPath "tools\$tool") `
        -r (Join-Path -Path $SCRIPT_DIR -ChildPath "tools\requirements.txt") `
        -p (Join-Path -Path $SCRIPT_DIR -ChildPath "tools")
}

# --- Orchestrate Connection Commands ---
orchestrate connections remove --app-id es_creds
orchestrate connections add -a es_creds

orchestrate connections configure -a es_creds --env draft --kind basic --type team

# Note: In PowerShell, environment variables are accessed via $env:VariableName
orchestrate connections set-credentials `
    -a es_creds `
    --env draft `
    -u $env:ELASTIC_USER `
    -p $env:ELASTIC_PASSWORD


# --- Import Agents ---
$agents = @(
    "packer.yaml",
    "terraform.yaml",
    "supervisor.yaml"
)

foreach ($agent in $agents) {
    orchestrate agents import -f (Join-Path -Path $SCRIPT_DIR -ChildPath "agents\$agent")
}