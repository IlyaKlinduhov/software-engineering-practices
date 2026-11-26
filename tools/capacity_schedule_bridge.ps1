$ErrorActionPreference = 'Stop'
$capacityGh = 'C:\Program Files\GitHub CLI\gh.exe'
$capacityRepo = 'IlyaKlinduhov/software-engineering-practices'
$capacityTask = 'StudyFlowProjectCapacityBridge'
$capacityLog = Join-Path $PSScriptRoot 'capacity-schedule-bridge.log'
function Write-CapacityLog([string]$Message) {
    Add-Content -LiteralPath $capacityLog -Value ((Get-Date).ToUniversalTime().ToString('o')+' '+$Message) -Encoding UTF8
}
try {
    $capacitySchedules = @(& $capacityGh run list --repo $capacityRepo --workflow project-capacity.yml --event schedule --limit 10 --json databaseId,conclusion,event,createdAt | ConvertFrom-Json)
    if ($LASTEXITCODE -ne 0) { throw 'Cannot read scheduled runs' }
    $capacityNativeSuccess = @($capacitySchedules | Where-Object { $_.conclusion -eq 'success' })
    if ($capacityNativeSuccess.Count -gt 0) {
        Write-CapacityLog ('Native GitHub schedule verified: '+$capacityNativeSuccess[0].databaseId+'; removing temporary bridge')
        Unregister-ScheduledTask -TaskName $capacityTask -Confirm:$false
        exit 0
    }
    $capacityRecentRuns = @(& $capacityGh run list --repo $capacityRepo --workflow project-capacity.yml --limit 1 --json databaseId,status,conclusion,createdAt | ConvertFrom-Json)
    if ($LASTEXITCODE -ne 0) { throw 'Cannot read latest capacity run' }
    if ($capacityRecentRuns.Count -gt 0) {
        $capacityLatest = $capacityRecentRuns[0]
        if ($capacityLatest.status -ne 'completed') {
            Write-CapacityLog ('Skipped: running workflow '+$capacityLatest.databaseId)
            exit 0
        }
    }
    & $capacityGh workflow run project-capacity.yml --repo $capacityRepo --ref main
    if ($LASTEXITCODE -ne 0) { throw 'Workflow dispatch failed' }
    Write-CapacityLog 'Dispatched cloud Project capacity workflow automatically from Windows timer'
} catch {
    Write-CapacityLog ('ERROR: '+$_.Exception.Message)
    exit 1
}
