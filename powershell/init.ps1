# Define the text to add to the $PROFILE file
$dockerToolsText = @"
# ----------
# DOCKER TOOLS
Set-Alias -Name de -Value ${PWD}\run.ps1
# ----------
"@

# Convert the $PROFILE file to a string
$profileString = [System.Text.Encoding]::Default.GetString([System.IO.File]::ReadAllBytes($PROFILE))

# Check if the $PROFILE file already contains the Docker tools text
if ($profileString.Contains($dockerToolsText)) {
    Write-Output "Docker tools is already installed."
} else {
    # Append the Docker tools text to the $PROFILE file
    Add-Content $PROFILE $dockerToolsText

    Write-Output "Docker tools has been installed."
}