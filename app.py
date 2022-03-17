from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json

browser = webdriver.Chrome(ChromeDriverManager().install())


def scraper():
    source = browser.page_source
    soup = BeautifulSoup(source, 'html.parser')

    all_records = soup.findAll('div', {"class": "panel panel-default m-b-md ng-scope"})
    results = []

    for i in range(len(all_records)):

        try:
            price = all_records[i].find('h3', {"class": "m-t-xs m-b-none m-l-sm font-bold text-muted ng-binding"}).text.split()[1].replace('$', '')
        except:
            price = None

        try:
            logos = all_records[i].findAll('img', {"class": "ng-scope"})
        except:
            logos = None
        try:
            flights_numbers = all_records[i].findAll('small', {"class": "clear font-bold ng-binding"})
        except:
            flights_numbers = None

        try:
            flight_info = all_records[i].findAll('div', {"class": "col-lg-8 col-md-8 col-sm-12 col-xs-12 no-padder"})
        except:
            flight_info = None

        flights = []
        for index in range(len(logos)):
            data = flight_info[index].findAll('div', {"class": "col-lg-3 col-md-3 col-sm-4 col-xs-4 m-t-xs m-b-xs text-ellipsis ng-binding"})

            flight = {

                "flight_number": flights_numbers[index].text,
                "logo": 'https://www.flyus.com/flights/' + logos[index].get('src'),

                "departure_time": data[0].text,
                "departure_date": data[1].text,
                "departure_airport": data[2].text,

                "arrival_time": data[3].text,
                "arrival_date": data[4].text,
                "arrival_airport": data[5].text,

            }
            flights.append(flight)

        result = {
            "price": price,
            "flights": flights,

        }
        results.append(result)

    file = json.dumps(results)
    with open("Results.json", "w") as outfile:
        outfile.write(file)

    browser.close()


link = 'https://www.flyus.com/flights/7HW-1/LHE-DXB/03-21-2022/1-0-0-Y'
browser.get(str(link))

time.sleep(10)  # wait to load the page content.
scraper()

