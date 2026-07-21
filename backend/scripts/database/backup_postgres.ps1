param(
    [Parameter(Mandatory=$true)]
    [string]$DatabaseUrl,

    [Parameter(Mandatory=$true)]
    [string]$OutputPath
)

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupFile = Join-Path $OutputPath "postgres-backup-$timestamp.dump"

pg_dump $DatabaseUrl --format=custom --file=$backupFile

Write-Host "Backup created: $backupFile"
