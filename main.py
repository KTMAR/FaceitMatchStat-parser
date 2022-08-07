import datetime
import json
import requests


def write_json(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def get_html(url):
    response = requests.get(url)
    json_string = json.loads(response.text)
    return json_string


url_hash_list = []


def get_url_hash(json_response):
    for i in json_response:
        url_hash_row = i['matchId']
        url_hash = f'https://api.faceit.com/stats/v1/stats/matches/{url_hash_row}'
        url_hash_list.append(url_hash)


def get_json_from_match_page(url):
    response = requests.get(url)
    json_format = json.loads(response.text)
    return json_format


def get_data_from_match_page(json_format, count):
    for i in json_format:
        match_id = i['_id']
        enemy_team = i['teams'][0]['players']
        allied_team = i['teams'][1]['players']
        times_row = i['date'] / 1000
        match_time = datetime.datetime.fromtimestamp(times_row).strftime("%d/%m/%Y, %H:%M:%S")
        match_map = i['i1']
        match_score = i['i18']
        region = i['i0']
        match_players = []

        for b in enemy_team:
            enemy_players = b['nickname']
            enemy_players_id = b['playerId']
            match_players.append(
                {'player': enemy_players,
                 'id': enemy_players_id,
                 })

        for b in allied_team:
            allied_players = b['nickname']
            allied_players_id = b['playerId']
            match_players.append(
                {'player': allied_players,
                 'id': allied_players_id,
                 })

        data = {
            'match_id': match_id,
            'time': match_time,
            'match_map': match_map,
            'match_score': match_score,
            'region': region,
            'match_players': match_players,

        }
        l1 = []

        for item in range(count):
            l1.append(data)

        write_json(l1)


def main():
    # 605955f4-f757-4221-b8f3-982fdf87b809
    # ^^ looks like this
    player_id = str(input('Player id: '))
    count = int(input('Number of matches: '))
    url = 'https://api.faceit.com/stats/v1/stats/time/users/' \
          f'{player_id}/games/csgo?page=1&size={count}'
    get_url_hash(get_html(url))

    for url in url_hash_list:
        get_data_from_match_page(get_json_from_match_page(url), count)


if __name__ == '__main__':
    main()
