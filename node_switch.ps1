param (
    [Parameter(Mandatory=$true)][string]$version=$(Read-Host "Enter the NVM Version")
)
$node_len=0
$nodejsdir="C:\Users\yathi\AppData\Roaming\nvm"
Write-Host "Selected Version=$version" -ForegroundColor Yellow
$nodejspath=$nodejsdir+"\v"+$version
Write-Host "Path=$nodejspath" -ForegroundColor Yellow
if (Test-Path -Path $nodejspath) {
   $node_len=[Environment]::GetEnvironmentVariable("NODE_PATH", "User").Length
   if ($node_len -eq 0) {
        Write-Host "Updating path Environment Varaible" -ForegroundColor Blue
        $Path = [Environment]::GetEnvironmentVariable("PATH", "User") + [IO.Path]::PathSeparator + "%NODE_PATH%" 
        [Environment]::SetEnvironmentVariable( "Path","$PATH", "User")
   }
   setx NODE_PATH "$nodejspath"
   exit 0
} else {
    "Node JS Version is not installed"
}
