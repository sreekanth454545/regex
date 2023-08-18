param (
    [Parameter(Mandatory=$true)][string]$version=$(Read-Host "Enter the NVM Version")
)
$nodejspath="C:\Users\yathi\AppData\Roaming\nvm"
Write-Host "Selected Version=$version" -ForegroundColor Yellow
$nodejspath=$nodejspath+"\v"+$version
Write-Host "Path=$nodejspath" -ForegroundColor Yellow
if (Test-Path -Path $nodejspath) {
    New-Item -ItemType SymbolicLink -Path "C:\Program Files\nodejs" -Target "$nodejspath" -Force
} else {
    "Node JS Version is not installed"
}
