import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import json
from pprint import pprint

URL = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'

link_vacancy = []
salary = []
res = []
des_vac = []
sort_list = []
company = []
city = []
end_list = []

def get_headers():
    return Headers(browser='chrome', os='mac').generate()

def page_link():
    main_padge = requests.get(URL, headers=get_headers()).text
    bs = BeautifulSoup(main_padge, features='lxml')
    vacancy = bs.find_all('a',  class_="serp-item__title")
    for vac in vacancy:
        link_vacancy.append(vac['href'])
        response_link_temp = requests.get(vac['href'], headers=get_headers()).text
        response_link = BeautifulSoup(response_link_temp, features='lxml')
        description = response_link.find('div', {'data-qa':'vacancy-description'})

        if (('Django'or'django' ) or ('Flask' or 'flask')) in description.text:
            des_vac.append('+')
        else:
            des_vac.append('-')

    for i, j in  zip(des_vac, link_vacancy):
        if i == '+':
            sort_list.append(j)
    return sort_list

def salary_search():
    for link in sort_list:
        salary_links = requests.get(link, headers=get_headers()).text
        salary_link = BeautifulSoup(salary_links, features='lxml')
        get_salary_link = salary_link.find('span', class_="bloko-header-section-2 bloko-header-section-2_lite")
        salary.append(get_salary_link.text.replace("\xa0", " "))
    return salary

def city_search():
    for link in sort_list:
        city_1 = requests.get(link, headers=get_headers()).text
        city_2 = BeautifulSoup(city_1, features='lxml')
        city_3 = city_2.find('span', {'data-qa':"vacancy-view-raw-address"})
        city_4 = city_2.find('p', {'data-qa': 'vacancy-view-location'})
        if city_3 != None:
            city.append(city_3.text)
        if city_4 != None:
            city.append(city_4.text)
    return city

def company_search():
    for link in sort_list:
        company_link_1 = requests.get(link, headers=get_headers()).text
        company_link_2 = BeautifulSoup(company_link_1, features='lxml')
        company_link_3 = company_link_2.find('span', {'data-qa': "bloko-header-2"}).text
        company.append(company_link_3.replace("\xa0", " "))
    return company

def sort_all(sort_list_all, salary, city, company):
    res = ({
        'link': sort_list_all,
        'salary' : salary,
        'city' : city,
        'company' : company
        })
    for i in range(len(res['city'])):
        if 'Москва' in res['city'][i] or 'Санкт-Петербург' in res['city'][i]:
            end_list.append({
                'Город': (res['city'][i]),
                'Компания': (res['company'][i]),
                'Сылка': (res['link'][i]),
                'Зарплата': (res['salary'][i])
                })
    return end_list



if __name__ == '__main__':
    page_link()
    salary_search()
    city_search()
    company_search()
    sort_all(sort_list, salary, city, company)

with open('vacancy.json', 'w', encoding='utf=8') as f:
    json.dump(end_list, f, indent=2, ensure_ascii=False)



