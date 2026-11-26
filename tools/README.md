# Резервный таймер пересчёта

Основное расписание находится в `.github/workflows/project-capacity.yml`: каждые пять минут на GitHub. При настройке 26.11.2026 первые запуски `schedule` задержались, поэтому добавлен временный таймер Windows `StudyFlowProjectCapacityBridge`.

Он работает каждые пять минут от текущего пользователя с ограниченными правами и вызывает `gh workflow run project-capacity.yml`. Сам расчёт выполняется в облачном GitHub Actions и читает Project. Токен Projects остаётся в Actions secret; таймер использует уже настроенный вход GitHub CLI. Окно PowerShell скрыто. Таймеру нужен включённый компьютер и выполненный вход в Windows; системная служба не создаётся.

Перед запуском таймер проверяет историю GitHub. Если уже есть успешный нативный `schedule`, он удаляет собственное задание Windows. Если расчёт уже идёт, повторный запуск пропускается. Период повторения ограничен 30 днями. Журнал находится рядом со скриптом в `capacity-schedule-bridge.log`; секреты туда не записываются.

Настройка: `powershell -File tools/install_capacity_bridge.ps1` из клона репозитория при настроенном `gh auth login`. Путь GitHub CLI в скрипте соответствует установке `C:\Program Files\GitHub CLI\gh.exe`.

Просмотр состояния: `Get-ScheduledTaskInfo -TaskName StudyFlowProjectCapacityBridge`.

Отключение: `Unregister-ScheduledTask -TaskName StudyFlowProjectCapacityBridge -Confirm:$false`.
