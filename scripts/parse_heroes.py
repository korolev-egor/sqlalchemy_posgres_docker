import json
from random import randint

import requests
from bs4 import BeautifulSoup


HERO_ATTRIBUTES = ['Strength', 'Agility', 'Intelligence']


def parse_table_from_soup(soup):
    data = []
    table = soup.find('table', attrs={'class':'wikitable'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    data = data[1]
    result = dict()
    for i, attribute in enumerate(HERO_ATTRIBUTES):
        result[attribute] = data[i].split('\n ')
    return result


def merge_radiant_with_dire(radiant, dire):
    def reformat_side_hero_data(side_data, side_name):
        result = dict()
        for attr in HERO_ATTRIBUTES:
            for hero in side_data[attr]:
                hero_information = dict()
                hero_information['attribute'] = attr
                hero_information['side'] = side_name
                hero_information['power'] = randint(0, 100)
                bio_request = requests.get(''.join(['https://dota2.fandom.com/wiki/', hero, '/Lore']))
                bio_soup = BeautifulSoup(bio_request.content, 'html.parser')
                try:
                    hero_bio = bio_soup.select('#mw-content-text > div > div:nth-child(2) > div:nth-child(2)')[0].get_text()
                except Exception:
                    continue
                hero_information['bio'] = hero_bio
                result[hero] = hero_information
        return result

    radiant = reformat_side_hero_data(radiant, 'radiant')
    dire = reformat_side_hero_data(dire, 'dire')
    return dict(**radiant, **dire)


def main():
    radiant_request = requests.get('https://dota2.fandom.com/wiki/Radiant')
    dire_request = requests.get('https://dota2.fandom.com/wiki/Dire')

    radiant_soup = BeautifulSoup(radiant_request.content, 'html.parser')
    dire_soup = BeautifulSoup(dire_request.content, 'html.parser')
    
    radiant_heroes = parse_table_from_soup(radiant_soup)
    dire_heroes = parse_table_from_soup(dire_soup)

    heroes = merge_radiant_with_dire(radiant_heroes, dire_heroes)

    with open('heroes.json', 'w') as file:
        json.dump(heroes, file)


if __name__ == '__main__':
    main()
