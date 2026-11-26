# Практические работы по программной инженерии

Проверено 24 ноября 2026 года. Все девять тем архива выполнены в варианте GitHub на самостоятельном проекте StudyFlow. Единственный незакрытый организационный пункт — приглашение 3–5 одногруппников из практики 1: их GitHub-логины не предоставлены.

[Код](https://github.com/IlyaKlinduhov/software-engineering-practices) · [Project](https://github.com/users/IlyaKlinduhov/projects/1) · [Wiki](https://github.com/IlyaKlinduhov/software-engineering-practices/wiki) · [Документация](https://github.com/IlyaKlinduhov/software-engineering-docs) · [Приложение](https://ilyaklinduhov.github.io/software-engineering-practices/)

## Практика 1 Создание проекта и совместная работа

Создан публичный репозиторий StudyFlow, задано описание, основная ветка main, включены Issues, Projects, Wiki и GitHub Actions. Добавлены самостоятельное приложение, тестовые данные и изображение проекта 1280×640. Для Wiki проверено ограничение редактирования участниками с правом записи. Профиль владельца использует существующий аватар.

Проверены страница репозитория, обложка и настройки Wiki. Код и история коммитов доступны в GitHub.

[Репозиторий](https://github.com/IlyaKlinduhov/software-engineering-practices)

Остаётся приглашение 3–5 одногруппников: их GitHub-логины не предоставлены. Этот пункт не отмечен выполненным. Организация Azure заменена личным репозиторием и Project владельца.

## Практика 2 Wiki и документация в репозитории

Созданы Home, начало работы, окружение разработки, команда, предстоящие события и страницы января/февраля. Боковое меню _Sidebar задаёт иерархию и порядок страниц. Страница окружения обновлена отдельным коммитом; в History сравнены исходная и уточнённая версии. Создан второй репозиторий документации: первоначальный README переименован в Our-team.md и затем дополнен отдельным коммитом. Добавлена вложенная папка Upcoming-events.

Проверены навигация Wiki, семь страниц, история и diff, а также шесть коммитов репозитория документации.

[Wiki](https://github.com/IlyaKlinduhov/software-engineering-practices/wiki) · [Документация в коде](https://github.com/IlyaKlinduhov/software-engineering-docs)

В GitHub нет Azure-функции публикации произвольной ветки как дополнительной Wiki. Её роль выполняет отдельный репозиторий Markdown. Вместо .order используются _Sidebar, оглавление README и префиксы 01/02.

## Подготовка 2 0 Подготовка тестовых данных

Созданы шесть демонстрационных учебных материалов и десять элементов backlog. Данные включают Epic, Feature, три пользовательские истории, две задачи и три истории для календаря поставок. В Issues добавлены описания, критерии приёмки, исполнитель, планы и внешние идентификаторы. Связана настоящая иерархия sub-issues: #1 → #2 → #3, #6, #7; #3 → #4, #5.

В репозитории доступны materials.json и backlog.json; в Project находятся десять основных элементов. Дополнительный Issue #11 использован только для проверки формы, закрыт и исключён из Project.

[Исходные данные](https://github.com/IlyaKlinduhov/software-engineering-practices/blob/main/backlog.json) · [Issues](https://github.com/IlyaKlinduhov/software-engineering-practices/issues)

Azure Demo Generator заменён самостоятельно подготовленным примером. Установка .NET, Azure и выпуск Full Access PAT для этого варианта не требуются.

## Практика 3 Scrum и управление ёмкостью

26 ноября 2026 года доступность и перегрузка связаны с настоящими данными GitHub Projects. В представлении «Загрузка Sprint 2» рядом с задачами #4 и #5 находится строка [Capacity] исполнителя IlyaKlinduhov. Её поля Assignees и «Итерация» определяют, какие задачи учитывать. «Часов в день» = 1, «Отпуск» = 2026-11-23..2026-11-27. Даты Sprint 2 берутся из поля итерации: 16.11–02.12.2026, 13 рабочих дней. После исключения пяти дней отпуска доступно 8 ч. Оценки задач 8 + 3 дают план 11 ч и перегрузку 3 ч.

Workflow Project capacity получает поля через GraphQL и записывает «Доступно, ч», «Запланировано, ч», «Перегрузка, ч» и время последнего расчёта обратно в Project. Проверены 14 тестов и успешный облачный CI. При снятии исполнителя с #4 автоматический запуск по событию Issues дал 8 / 3 / 0. При возвращении исполнителя, оценке #4 = 5 и доступности 2 ч/день следующий автоматический запуск дал 16 / 8 / 0. Затем восстановлены оценка 8 и доступность 1 ч/день. Автоматический запуск при обновлении workflow #45835119426 подтвердил восстановленные 8 / 11 / 3. Пересчёт срабатывал в облаке на настоящих данных, локальный скрипт при этих проверках не запускался. Расписание включено, но первый запуск с событием schedule на момент проверки ещё не получен; его фактическое выполнение отдельно пока не подтверждено.

[Живая загрузка](https://github.com/users/IlyaKlinduhov/projects/1/views/3) · [Автоматический запуск: восстановленные данные](https://github.com/IlyaKlinduhov/software-engineering-practices/actions/runs/45835119426) · [Проверка изменения входных данных](https://github.com/IlyaKlinduhov/software-engineering-practices/actions/runs/45833683897) · [Код пересчёта](https://github.com/IlyaKlinduhov/software-engineering-practices/blob/main/project_capacity.py) · [Workflow](https://github.com/IlyaKlinduhov/software-engineering-practices/actions/workflows/project-capacity.yml) · [Инструкция](https://github.com/IlyaKlinduhov/software-engineering-practices/blob/main/PLANNING.md)

Изменения пользовательских полей персонального Project обрабатываются расписанием каждые 5 минут; GitHub может задерживать фактический запуск. Изменение исполнителя и закрытие/открытие Issue также запускают пересчёт. Вручную запускать код при планировании не требуется. Дата UTC и ссылка на последний запуск видны в поле «Расчёт загрузки», JSON — в артефакте запуска, таблица — в Summary. Classic-токен имеет только scope project, хранится в Actions secret PROJECTS_TOKEN и истекает 26.12.2026; после истечения его нужно заменить. Статичный пример приложения подписан отдельно и не используется как источник живой загрузки. Задача #4 оставлена в Sprint 2.

## Практика 4 Kanban и настройка процесса

Настроены шесть этапов Backlog, Approved, Committed, QA Doing, QA Done и Done. Для QA Doing установлен WIP 1. Созданы дорожки Обычная и Ускорение, цветные метки данные, ux/ui, development и Ускорение; на карточках видны дополнительные поля и Ticket ID. Критерии готовности записаны в описании процесса и этапа QA Done. Сохранены обзор спринта, веб-задачи и срочная дорожка. В Insights находятся три диаграммы.

Проверено превышение WIP: временно в QA Doing находились две задачи, GitHub показал красное 2/1; после проверки восстановлен итоговый статус #5 Committed. Форма Product Backlog Item проверена созданием #11 с SF-PBI-011, затем контрольная карточка закрыта. Диаграммы показывают статусы семи элементов Sprint 2, 11 часов нагрузки и две веб-задачи.

[Kanban](https://github.com/users/IlyaKlinduhov/projects/1/views/2) · [Обзор Sprint 2](https://github.com/users/IlyaKlinduhov/projects/1/insights/1) · [Нагрузка](https://github.com/users/IlyaKlinduhov/projects/1/insights/2) · [Веб-задачи по исполнителям](https://github.com/users/IlyaKlinduhov/projects/1/insights/3) · [Проверка формы](https://github.com/IlyaKlinduhov/software-engineering-practices/issues/11)

Split column заменён двумя статусами QA Doing/QA Done. Наследуемый Scrum-процесс заменён полями Project и YAML-формой с обязательными Ticket ID, описанием, критериями приёмки и активностью.

## Практика 5 Календарь поставок двух команд

Создан Roadmap с датами Начало/Окончание и группировкой по StudyFlow Web и External integrations. Для внешней команды заданы Итерация 50 с 24 ноября по 11 декабря, перерыв 12–13 декабря и Итерация 51 с 14 декабря по 1 января. Корпоративная интеграция #8 перенесена в первую поставку, погодная #9 — во вторую, зависимое отслеживание #10 — в Sprint 4 после готовности #8. Создана веха Команда в отпуске на последнюю пятницу месяца, 27 ноября.

В календаре видны две команды, девять незавершённых элементов, маркеры спринтов, поставок и контрольной вехи. Фильтр -status:Done скрывает #7. Автотест сначала выявляет конфликт зависимости, затем подтверждает его устранение.

[Календарь](https://github.com/users/IlyaKlinduhov/projects/1/views/7) · [Контрольная веха](https://github.com/IlyaKlinduhov/software-engineering-practices/milestone/1) · [Зависимая задача](https://github.com/IlyaKlinduhov/software-engineering-practices/issues/10)

Команды реализованы полем Project и группами Roadmap. Это учебные направления работы, а не вымышленные аккаунты участников. Неиспользуемая автоматически созданная Поставка 3 оставлена резервной.

## Практика 6 Собственный обработчик GitHub Actions

С официальной страницы GitHub получен Windows x64 runner 2.338.2; SHA256 архива проверен. Обработчик studyflow-windows зарегистрирован для учебного репозитория с labels self-hosted, Windows, X64, studyflow. Запущен пользовательским процессом без системной службы. Ручной workflow получил код, показал возможности обработчика, выполнил семь тестов и сборку.

Контрольный запуск #45464936988 завершился Success; задание smoke выполнялось 27 секунд. После одного задания ephemeral runner автоматически снялся с регистрации, удалил .runner/.credentials и завершил процесс. Токен регистрации не включён в репозиторий или отчёты.

[Успешный запуск](https://github.com/IlyaKlinduhov/software-engineering-practices/actions/runs/45464936988) · [Workflow](https://github.com/IlyaKlinduhov/software-engineering-practices/blob/main/.github/workflows/self-hosted-smoke.yml)

Runner намеренно одноразовый; для повторного показа живого обработчика потребуется новая регистрация на странице Settings → Actions → Runners. В запуске checkout есть два предупреждения invalid pattern при работе с временным Windows-путём Git; тесты и сборка завершились успешно.

## Практика 7 Непрерывная интеграция

Создан Continuous integration с событиями push в main и workflow_dispatch, Python 3.12, семью тестами и production-сборкой. Результат публикуется как studyflow-dist с SHA коммита; хранение 30 дней. Заголовок template.html изменён отдельным коммитом через веб-интерфейс GitHub, что автоматически запустило новый CI.

Коммит e1966202c3ed590342e7e30ded731e14169a87b7 вызвал запуск #45468359294, результат Success. Отдельный ручной запуск #45469745957 также завершился Success. На странице автоматического запуска присутствует артефакт 4 KB, SHA256 55aa257e3564ef8d9fb919878465979757bc15a9a102929f8e7343751f98d4c6. Локально семь тестов также прошли.

[Автоматический CI](https://github.com/IlyaKlinduhov/software-engineering-practices/actions/runs/45468359294) · [Ручной CI](https://github.com/IlyaKlinduhov/software-engineering-practices/actions/runs/45469745957) · [Коммит-триггер](https://github.com/IlyaKlinduhov/software-engineering-practices/commit/e1966202c3ed590342e7e30ded731e14169a87b7) · [Workflow](https://github.com/IlyaKlinduhov/software-engineering-practices/blob/main/.github/workflows/ci.yml)

Для регулярного CI используется облачный runner; собственный Windows runner отдельно проверен в практике 6. Внешних Python-зависимостей нет, поэтому этап восстановления пакетов не требуется.

## Дополнение 4 2 Многоэтапный YAML и автоматическая доставка

Создан Build and deploy StudyFlow. Этап build получает исходники, выполняет тесты и сборку, затем передаёт Pages artifact. Этап deploy зависит от build через needs и публикует тот же результат в GitHub Pages. Для deploy заданы отдельные разрешения pages:write и id-token:write; build получает contents:read.

Автоматический запуск #45468359550 после изменения заголовка завершил build и deploy успешно. Опубликованный сайт открылся с новым заголовком StudyFlow — каталог по программной инженерии. В браузере проверены поиск Kanban, выбор темы Инструменты, сообщение о пустом результате, запись просмотра и сохранение истории после перезагрузки.

[Успешная поставка](https://github.com/IlyaKlinduhov/software-engineering-practices/actions/runs/45468359550) · [Приложение](https://ilyaklinduhov.github.io/software-engineering-practices/) · [YAML](https://github.com/IlyaKlinduhov/software-engineering-practices/blob/main/.github/workflows/delivery.yml)

Azure Web App + SQL заменён статическим приложением GitHub Pages с JSON-данными и историей в браузере. Облачная SQL-база не создавалась; это явно указанное отличие реализации. Платные ресурсы Azure отсутствуют.

## Документация платформы

- [Python в GitHub Actions](https://docs.github.com/en/actions/tutorials/build-and-test-code/python)
- [Многоэтапная публикация Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- [Self-hosted runners](https://docs.github.com/actions/hosting-your-own-runners/about-self-hosted-runners)
