# SaindBot

Это мой Telegram-бот, который я планирую развивать как pet-проект.

На текущий момент у него нет никакой цели. Я всего лишь пробую кодить на Python и использовать разные функции.

Есть желание попробовать накрутить в него осмысленных операций по работе с GPT и разными сервисами с открытыми API, для
обучения работы с интеграциями. Также в планах добавить в боте возможность хранения данных о пользователях (
БД/excel/файл - \"\"\\\_(0_0)_/"").

---
_Начальная версия этого бота создана на базе бесплатных эфиров от Skillbox, буткемп "Python для всех: практический
мини-курс для новичков"._

# Использование бота

## Установка пакетов

Тебе, конечно же, потребуется <a href=https://www.python.org/downloads/>установить Python</a> _(я использую v3.11.4)_.
В том числе, установить библиотеки указанные в файле **requirements.txt**.

Для установки библиотек ты можешь использовать команду, в терминале:

```commandline
pip install name_packege
```

## Создание бота

Также, тебе понадобится создать своего собственного бота с помощью <a href=https://t.me/BotFather>BotFather</a>.
После создания бота, создай файл `token.txt` и сохрани в нём свой **token** или вставь его непосредственно в
строке `token = 'your_token'`, не забудь удалить граничные строки.

## Запуск бота

Для запуска программы выполни команду в терминале:

```commandline
Python your_path_project\name_programm.py
```

Бот будет работать локально у тебя на компьютере. Пока запущена программа бот будет отвечать на вызовы. Для работы 24/7
тебе понадобится развернуть его на сервере.
Я для этого использую сервис <a href=https://www.pythonanywhere.com/>PythonAnywhere</a>.