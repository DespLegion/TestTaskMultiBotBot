# Тестовое задание: Разработка чат-бота с набором инструментов для Telegram

## Задача:
Создать чат-бота для личных сообщений Telegram, предлагающего пользователю простой набор инструментов.

## Функциональность:
1) Получение информации извне (прогноз погоды, курс валют, случайная картинка котика и т.д.).
2) Редактирование присланного пользователем фото и отправка измененной картинки обратно.
3) Прохождение теста с выбором ответов и выдача результата.
4) To-DO List:
    1) Добавление задачи
    2) Удаление задачи
    3) Просмотр списка задач
    4) Изменение задачи

### Пользовательский путь:

#### Старт:
- Пользователь входит в бота, отправляет стартовую команду.
- Получает сообщение-меню с кнопкой, которая ведёт на активность.
#### Информационные запросы:
- При выборе соответствующей кнопки (например, прогноз погоды) пользователь сразу получает запрошенную информацию.
- Следом пользователю предлагается вернуться в меню.
#### Изменение фотографии:
- При выборе соответствующей активности бот ожидает от пользователя фотографию.
- После получения, бот обрабатывает изображение (обрезка/масштабирование, наложение рамки) и отправляет его обратно пользователю.
- Пользователь получает сообщение с меню.
#### Прохождение теста:
- При выборе теста пользователю поочерёдно приходят вопросы с вариантами ответов в виде кнопок.
- После выбора ответа пользователь получает следующий вопрос.
- По завершении теста анализируются ответы и выдаётся результат.
- После выдачи результата пользователю предлагается вернуться в меню.
#### TO-DO List:
- Добавление задачи:
    - При нажатии на "Добавить задачу", пользователь последовательно вводит заголовок задачи, описание задачи, и выбирает "Сохранить" для добавления в список или "Отменить".
- Просмотр списка задач:
    - При нажатии на "Список задач", бот показывает список задач пользователя, который может быть представлен текстовым сообщением с номерами и заголовками задач или кнопками с заголовками задач.
- Выбор и управление задачей:
    - Для текстового списка пользователь вводит номер задачи для её выбора.
    - Для списка с кнопками нажимает на кнопку с нужной задачей.
    - После выбора задачи пользователю показывается полный текст задачи с двумя кнопками: "Удалить задачу" и "Изменить задачу".
    - При нажатии "Удалить задачу" задача удаляется из списка.
    - При нажатии "Изменить задачу" начинается процесс редактирования, аналогичный добавлению новой задачи, но для существующей.

### Важные нюансы:
- Многопользовательская поддержка: бот должен корректно работать с несколькими пользователями одновременно.
- Постоянство данных: информация и результаты действий пользователей не должны теряться при перезапуске бота, все данные должны сохраняться в БД.
- Использование Django для работы с базой данных и административных функций приветствуется.

__________


# Реализация задания
### Данный репозиторий является `frontend` (Ботом) частью задания. Ссылка на `backend`: [backend](https://github.com/DespLegion/TestTaskMultiBotBackend)

## В `frontend` использовались следующие технологии:
### `Aiogram` + `Aiohttp`
### В качестве базы данных используется `PostgreSQL`


Проект построен на небольших независимых приложениях (пародия на микросервисы :) ).
Благодаря этому его очень легко масштабировать (добавлять новые приложения) и убирать часть функционала
(удалять приложения). В глобальном плане - это ни как не скажется на работе всего проекта
и на работе других приложений

#### Bot Commands:

В боте используется только одна команда - Стартовая:

`/start`

Все остальное взаимодействие с пользователем происходит исключительно в интерактивном режиме

#### Запуск Бота

Точкой входа в бота является файл `bot_start.py`
