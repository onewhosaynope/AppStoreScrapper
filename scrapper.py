from datetime import datetime, timedelta
from helpers import check
from bs4 import BeautifulSoup
import requests
from requests.exceptions import Timeout
from data import categories

def scrap(url):

    response = requests.get(url)
    print('Url: ' + url + '\nCode: ' + str(response.status_code))

    content = response.content

    soup = BeautifulSoup(content, "xml")
    entry = soup.find_all('entry')

    current_date = datetime.now()

    current_time = current_date.strftime("%H")

    if int(current_time) < 11:
        current_date = current_date - timedelta(days=1)

    current_date_ru = current_date.strftime('%d.%m.%Y')
    current_date_us_m = current_date.strftime("%B") # current date
    current_date_us_d = current_date.strftime("%d") # current date
    current_date_us_y = current_date.strftime("%Y") # current date
    if (current_date_us_d[0] == '0'):
        current_date_us_d = current_date_us_d.replace('0', '')
    current_date_us = current_date_us_m + ' ' + current_date_us_d + ', ' + current_date_us_y
    
    result = []

    for item in entry:

        title = item.find('im:releaseDate')
        release_date = title.get('label')
            
        if release_date == current_date_us or release_date == current_date_ru:
            author = item.find('im:artist').text # author name
            
            if check(author):

                title = item.find('im:name').text # app name
                
                price = item.find('im:price')
                if price.get('amount') == '0.00000':
                    cost = "FREE"
                else:
                    cost = str(price.get('amount')[:-3] + price.get('currency'))
                
                app_link = str(item.find('link').get('href'))
                app_link_ru = app_link.replace('/us/', '/ru/')
                app_link_us = app_link.replace('/ru/', '/us/')

                category = item.find('category').get('label')

                if category in categories.keys():
                    category = categories[category]


                author_link= str(item.find('im:artist').get('href'))

                print(author_link)

                if author_link == "None":
                    author_link_ru = "None"
                    author_link_us = "None"

                else:
                    author_link_ru = author_link.replace('/us/', '/ru/')
                    author_link_us = author_link.replace('/ru/', '/us/')

                    # try:
                    #     response_ru = requests.get(author_link_ru)
                    # except Timeout:
                    #     response_ru = "request timeout"
                    
                    # try:
                    #     response_us = requests.get(author_link_us)
                    # except Timeout:
                    #     response_ru = "request timeout"

                    # if response_ru != "<Response [200]>":
                    #     author_link_ru = 'None'
                    # if response_us != "<Response [200]>":
                    #     author_link_us = 'None'


                entity = {
                    'title': title, 
                    'cost': cost, 
                    'app_link_ru': app_link_ru,
                    'app_link_us': app_link_us, 
                    'category': category, 
                    'author': author, 
                    'author_link_ru': author_link_ru,
                    'author_link_us': author_link_us,
                    'release_date': current_date_us}
                
                if entity not in result:
                    result.append(entity)

        else:
            break

    return result