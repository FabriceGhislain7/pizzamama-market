param(
    [Parameter(Mandatory=$true)]
    [string]$DatabaseUrl,

    [Parameter(Mandatory=$true)]
    [string]$BackupFile
)

# ATTENZIONE: non eseguire mai su production direttamente.
# Testare sempre su staging o database temporaneo prima.

pg_restore --clean --if-exists --no-owner --dbname=$DatabaseUrl $BackupFile

Write-Host "Restore completed from: $BackupFile"
