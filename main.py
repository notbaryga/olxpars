import requests
from bs4 import BeautifulSoup as BS
import csv

def get_positions(url: str) -> list:
  page = requests.get(url)
  soup = BS(page.text, "html.parser")
  ans: list = []
  for advert in soup.findAll(class_='css-1sw7q4x'):
    for el in advert.findAll(class_='css-rc5s2u'):
        ans.append(el)
  return ans

def get_information_about(position) -> dict:
  s = {}
  s['Name'] = position.find(class_ = 'css-16v5mdi er34gjf0').text
  s['Price'] = position.find(class_ = 'css-10b0gli er34gjf0').text
  try:
    s['State'] = position.find(class_ = 'css-3lkihg').get('title')
  except:
    s['State'] = 'Не указано'
  s['Location'], s['Date'] = position.find(class_ = 'css-veheph er34gjf0').text.split(' - ')
  s['Link'] = 'https://www.olx.kz' + position.get('href')
  return s

def get_category_pages(url: str, ans: list) -> list:
  page = requests.get(url)
  soup = BS(page.text, "html.parser")
  
  next_url = 'https://www.olx.kz' + soup.find(class_='css-j8u5qq').findAll('a')[-1].get('href')
  if next_url != url:
    ans.append(next_url)
    #print(ans)
    #print(next_url)
    get_category_pages(next_url, ans)
  else:
    #print('blya')
    print(ans)
    b = ans
    return b

def main():
    categories, names = ['https://www.olx.kz/d/moda-i-stil/krasota-zdorove/parfyumeriya/', 'https://www.olx.kz/d/moda-i-stil/podarki/vkusnye/'], ['Парфюмерия', 'Подарки']
    fields = ['Name', 'Price', 'State', 'New price', 'Location', 'Date', 'Link']

    for i in range(len(categories)):
        positions = []
        links = get_category_pages(categories[i], [])
        for er in links:
          for el in get_positions(er):
              positions.append(get_information_about(el))

        with open(f'{names[i]}.csv', 'a', newline='', encoding='UTF-8') as f:
            writer = csv.DictWriter(f, fields)
            writer.writerows(positions)

def main2():
  print(get_category_pages('https://www.olx.kz/d/moda-i-stil/krasota-zdorove/parfyumeriya/', []))

if __name__ == '__main__':
    main2()