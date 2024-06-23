from typing import List, Tuple

from db.connect import connect_to_db


class DBManager:
    def __init__(self):
        """
        Инициализация соединения с базой данных
        """
        self.cursor = connect_to_db().cursor()

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """
        Получение списка всех компаний и количества вакансий у каждой компании

            :return Список кортежей, где каждый кортеж содержит название компании и количество вакансий
        """

        query = """
            SELECT c.company_name, COUNT(v.id) AS vacancy_count
            FROM companies c
            LEFT JOIN vacancies v ON c.company_name = v.company_name
            GROUP BY c.company_name;
        """

        self.cursor.execute(query)
        result = self.cursor.fetchall()

        return result

    def get_all_vacancies(self) -> List[Tuple[str, str, int, str]]:
        """
        Получение списка всех вакансий с деталями: название компании, название вакансии, зарплата, ссылка

            :return Список кортежей, где каждый кортеж содержит название вакансии, название компании, зарплату и
                    ссылку на вакансию
        """

        query = """
            SELECT v.name, c.company_name, v.salary, v.url
            FROM vacancies v
            JOIN companies c ON v.company_name = c.company_name;
        """

        self.cursor.execute(query)
        result = self.cursor.fetchall()

        return result

    def get_avg_salary(self) -> float:
        """
        Получение средней зарплаты по всем вакансиям

            :return Средняя зарплата по всем вакансиям
        """

        query = """
            SELECT AVG(salary) FROM vacancies;
        """

        self.cursor.execute(query)
        avg_salary = self.cursor.fetchone()[0]

        return avg_salary

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, str, int, str]]:
        """
        Получение списка вакансий с зарплатой выше средней по всем вакансиям

            :return Список кортежей, где каждый кортеж содержит название вакансии, название компании,
                    зарплату и ссылку на вакансию
        """
        avg_salary = self.get_avg_salary()

        query = """
            SELECT v.name, c.company_name, v.salary, v.url
            FROM vacancies v
            JOIN companies c ON v.company_name = c.company_name
            WHERE v.salary > %s;
        """

        self.cursor.execute(query, (avg_salary,))
        result = self.cursor.fetchall()

        return result

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[str, str, int, str]]:
        """
        Получение списка вакансий, название которых содержит указанное ключевое слово.

            :param keyword: Ключевое слово для поиска в названии вакансии.
            :return Список кортежей, где каждый кортеж содержит название вакансии, название компании, зарплату
                    и ссылку на вакансию
        """

        query = """
            SELECT v.name, c.company_name, v.salary, v.url
            FROM vacancies v
            JOIN companies c ON v.company_name = c.company_name
            WHERE v.name ILIKE %s;
        """

        self.cursor.execute(query, (f'%{keyword}%',))
        result = self.cursor.fetchall()

        return result
