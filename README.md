# Данные о курсах на Курсере

Скрипт собирает данные о курсах на [coursera.org](https://www.coursera.org/) и сохраняет их в .xlsm фаил в указанную папку.

Колличество курсов: 20

Тип данных: название, язык (включая субтитры), дату начала, длительность (в неделях), рейтинг, ссылку.

# Как работает 
```bash
$ python coursera.py A:\myfiles
Файл сохранен
A:\myfiles\courses.xlsx
```

# Требования
Совестимые OC:
* Linux,
* Windows
* MacOS

Скрипт требует для своей работы установленного интерпретатора Python версии 3.5 выше

И  пакетов из requirements.txt
```bash
pip install -r requirements.txt # или командой pip3
```
# Как запустить
Стандатной командой `python` (на некоторых компьютерах `python3`)

```bash
$ python coursera.py [-h] filedir
 
positional arguments:
  filedir     Путь для сохранения файла
 
optional arguments:
  -h, --help  show this help message and exit
```
> Запуск для всех ОС одинаковый

Помните, рекомендуется использовать [virtualenv/venv](https://devman.org/encyclopedia/pip/pip_virtualenv/) для лучшего управления пакетами.

# Цели проекта
Код создан в учебных целях. В рамках учебного курса по веб-разработке - [DEVMAN.org](https://devman.org)