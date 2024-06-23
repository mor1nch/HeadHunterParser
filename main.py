import json

from api.hh_api import HeadHunterApi
from db.create import create_tables
from db.fill import fill_data

if __name__ == "__main__":
    url = "https://api.hh.ru/vacancies"
    hh_api = HeadHunterApi(url)
    companies = hh_api.get_companies_vacancies({'per_page': 50})

    with open('companies.json', 'w', encoding='utf-8') as file:
        json.dump(companies, file, ensure_ascii=False)

    create_tables()
    fill_data()
