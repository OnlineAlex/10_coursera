import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import os
import argparse


def is_valid_path(argument_path):
    if not os.path.exists(argument_path):
        error_message = 'Папка {} не существует'.format(argument_path)
        raise argparse.ArgumentTypeError(error_message)

    return argument_path


def get_filedir():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filedir',
        type=is_valid_path,
        help='Путь для сохранения файла'
    )
    return parser.parse_args()


def get_courses_list(number_courses):
    response = requests.get(
        'https://www.coursera.org/sitemap~www~courses.xml',
    )
    courses_xml = BeautifulSoup(response.content, features='xml')
    courses = courses_xml.text.split()
    return courses[:number_courses]


def get_course_info(course_url):
    response = requests.get(course_url)
    response.encoding = 'utf-8'
    course_code = BeautifulSoup(response.text, 'html.parser')
    startdate_text = course_code.select_one('.startdate').text
    rating = course_code.select_one('.ratings-text')
    if rating:
        rating = rating.text[:3]

    return {
        'title': course_code.select_one('.title').text,
        'language': course_code.select_one('.rc-Language').text,
        'date start': startdate_text[startdate_text.find(' ')+1:],
        'number week': len(course_code.select('.week')),
        'rating': rating,
        'url': course_url
    }


def get_colums_max_width(table):
    colums_width = {}
    for row in table.rows:
        for cell in row:
                colums_width[cell.column] = max((
                    colums_width.get(cell.column, 0),
                    len(str(cell.value))
                ))
    return colums_width


def output_courses_info_to_xlsx(courses, filepath):
    courses_workbook = Workbook()
    courses_sheet = courses_workbook.active
    courses_sheet.append([
        'Название',
        'Язык',
        'Дата начала',
        'Длительность (нед)',
        'Средняя оценка',
        'Ссылка'
    ])

    for course in courses:
        courses_sheet.append([
            course['title'],
            course['language'],
            course['date start'],
            course['number week'],
            course['rating'],
            course['url']
        ])

    colums_max_width = get_colums_max_width(courses_sheet)
    for column, value in colums_max_width.items():
        courses_sheet.column_dimensions[column].width = value

    courses_workbook.save(filepath)
    if os.path.exists(filepath):
        return True


if __name__ == '__main__':
    arguments = get_filedir()
    xlsx_filepath = os.path.join(arguments.filedir, 'courses.xlsx')

    try:
        courses_list = get_courses_list(number_courses=20)
        courses_info = []
        for course in courses_list:
            courses_info.append(get_course_info(course))
    except requests.ConnectionError:
        exit('Не удалось подключиться к серверу\n'
             'Проверьте интернет соеденние')

    if output_courses_info_to_xlsx(courses_info, xlsx_filepath):
        print('Файл сохранен\n{}'.format(xlsx_filepath))
    else:
        print('Что-то пошло не так. Файл не сохранен.')

