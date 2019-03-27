import json
import urllib.request
import sys


def get_weather(city):
    with open('city.list.json') as file:
        data = json.load(file)
    
    dict = {}
    counter = 0
    for d in data:
        if city == d.get('name'):
            counter += 1
            dict[str(counter)] = d

    if not dict:
        return "City '{}' isn't in the database".format(city)

    if len(dict) == 1:
        id_city = dict[str(counter)]['id']
    else:
        print("{:<8} {:<10} {:<10} {:<10} {:<10}".format('Key', 'ID', 'Name', 'Country', 'Coord'))
        for key, value in dict.items():
            id, name, country = value['id'], value['name'], value['country']
            coord = '{lat}, {lon}'.format(**value['coord'])
            print("{:<8} {:<10} {:<10} {:<10} {:<10}".format(key, id, name, country, coord))
        select_city = input('Which city do you choose? Please, select KEY: ')
        id_city = dict[select_city]['id']
    
    try:
        url = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?id={}&units=metric&APPID=43d563f5fbc69461e0b11f3fc3b90b3f'.format(id_city))
        data = json.loads(url.read().decode())
        temp = str(data['main']['temp'])
        return '{} °C'.format(temp)
    except urllib.error.HTTPError:
        return "HTTP Error 400: Bad Request - no URL for ID: {}".format(id_city)


def check_input_city(argv):
    if len(argv) == 1 and len(argv[0]) <= 2:
        print('To few letters')
    elif len(argv) == 1:
        city = argv[0]
        return city.title()
    
    while True:
        select_city = input('The get_weather() function requires 1 argument. Your argument is: ')
        if len(select_city) >= 2:
            return select_city.title()
        print('To few letters.')


if __name__ == '__main__':
    print(get_weather(check_input_city(sys.argv[1:])))



