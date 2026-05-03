# PowerShell Script to setup winutils for Spark on Windows
$ErrorActionPreference = 'Stop'

$hadoopHome = "$PSScriptRoot\hadoop"
$binDir = "$hadoopHome\bin"

Write-Host "Setting up Hadoop home for winutils at $hadoopHome"

if (-not (Test-Path $binDir)) {
    New-Item -ItemType Directory -Force -Path $binDir | Out-Null
    Write-Host "Created directory $binDir"
}

# Download winutils.exe for Hadoop 3.0.0
$winutilsUrl = "https://github.com/steveloughran/winutils/raw/master/hadoop-3.0.0/bin/winutils.exe"
$winutilsPath = "$binDir\winutils.exe"

if (-not (Test-Path $winutilsPath)) {
    Write-Host "Downloading winutils.exe..."
    Invoke-WebRequest -Uri $winutilsUrl -OutFile $winutilsPath
    Write-Host "winutils.exe downloaded."
} else {
    Write-Host "winutils.exe already exists."
}

# Download hadoop.dll for Hadoop 3.0.0
$hadoopDllUrl = "https://github.com/steveloughran/winutils/raw/master/hadoop-3.0.0/bin/hadoop.dll"
$hadoopDllPath = "$binDir\hadoop.dll"

if (-not (Test-Path $hadoopDllPath)) {
    Write-Host "Downloading hadoop.dll..."
    Invoke-WebRequest -Uri $hadoopDllUrl -OutFile $hadoopDllPath
    Write-Host "hadoop.dll downloaded."
} else {
    Write-Host "hadoop.dll already exists."
}

# Set Environment Variables for the current session
$env:HADOOP_HOME = $hadoopHome
$env:Path += ";$binDir"

Write-Host ""
Write-Host "Setup complete!"
Write-Host "To make HADOOP_HOME permanent, you can add it to your System Environment Variables."
Write-Host "Path to HADOOP_HOME: $hadoopHome"
Write-Host "Run this script before running PySpark if HADOOP_HOME is not set globally."
