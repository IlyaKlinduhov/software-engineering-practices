$ErrorActionPreference = 'Stop'
$capacityScript = Join-Path $PSScriptRoot 'capacity_schedule_bridge.ps1'
$capacityPowerShell = Join-Path $env:SystemRoot 'System32/WindowsPowerShell/v1.0/powershell.exe'
$capacityAction = New-ScheduledTaskAction -Execute $capacityPowerShell -Argument ('-NoLogo -NoProfile -NonInteractive -WindowStyle Hidden -File "'+$capacityScript+'"') -WorkingDirectory $PSScriptRoot
$capacityTrigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration (New-TimeSpan -Days 30)
$capacityPrincipal = New-ScheduledTaskPrincipal -UserId ([Security.Principal.WindowsIdentity]::GetCurrent().Name) -LogonType Interactive -RunLevel Limited
$capacitySettings = New-ScheduledTaskSettingsSet -Hidden -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 3)
Register-ScheduledTask -TaskName 'StudyFlowProjectCapacityBridge' -Action $capacityAction -Trigger $capacityTrigger -Principal $capacityPrincipal -Settings $capacitySettings -Description 'Temporary StudyFlow cloud workflow timer; removes itself after native GitHub schedule succeeds; expires after 30 days.'
