@echo off
set  version=%1
echo "Selected Version:%version%"
IF "%version%"=="" (
    echo "Error Invalid Arguments"
) ELSE (
    C:\Windows\System32\runas.exe /user:YATHISH-PC\yathi "C:\Users\%USERNAME%\AppData\Roaming\nvm use %version%"
    echo "Done"
)
