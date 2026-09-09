$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
python -m PyInstaller --noconfirm --clean --onefile --windowed --name MLCalculator --icon icon.ico --add-data 'www;www' --hidden-import webview --collect-submodules webview --exclude-module tkinter main.py
if ($LASTEXITCODE -ne 0) { throw 'Build failed' }
