import json
from psycopg2 import errors

from db.connect import connect_to_db


def connection(func):
    """
    Декоратор для управления соединением с базой данных и транзакциями.

        :param func: Функция, которую нужно выполнить в рамках транзакции.
        :return wrapper: Обёртка для выполнения функции с управлением соединением и транзакциями.
    """

    def wrapper(*args, **kwargs):
        connection = connect_to_db()
        cursor = connection.cursor()

        try:
            func(*args, **kwargs, cursor=cursor)
            connection.commit()
        except errors.UniqueViolation:
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    return wrapper


@connection
def insert_company(name: str, cursor) -> None:
    """
    Вставка новой компании в таблицу companies.

        :param name: Название компании.
        :param cursor: Курсор для выполнения SQL-запроса.
    """

    cursor.execute("""
        INSERT INTO companies (company_name)
        VALUES (%s);
    """, (name,))


@connection
def insert_vacancy(name: str, salary: int, url: str, company_name: str, cursor) -> None:
    """
    Вставка новой вакансии в таблицу vacancies.

        :param name: Название вакансии.
        :param salary: Зарплата.
        :param url: URL вакансии.
        :param company_name: Название компании, к которой относится вакансия.
        :param cursor: Курсор для выполнения SQL-запроса.
    """

    cursor.execute("""
        INSERT INTO vacancies (name, salary, url, company_name)
        VALUES (%s, %s, %s, %s) RETURNING id;
    """, (name, salary, url, company_name))


def fill_data():
    """
    Заполнение базы данных данными из JSON-файла.
    """
    with open("../companies.json", "r", encoding="utf-8") as file:
        data = json.load(file)

        for company in data:
            insert_company(company['company_name'])

            for vacancy in company['vacancies']:
                insert_vacancy(
                    vacancy["name"],
                    vacancy["salary"],
                    vacancy["url"],
                    vacancy["company_name"]
                )
