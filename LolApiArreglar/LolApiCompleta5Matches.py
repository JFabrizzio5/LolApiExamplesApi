import requests

# Configura tu API Key y la región
api_key = 'RGAPI-4a1c3d23-1048-4875-939d-88787fbea1e2'
region = 'americas'

def get_puuid(game_name, tag_line):
    url = f'https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}?api_key={api_key}'
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "es-419,es;q=0.9,es-ES;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        account_info = response.json()
        return account_info['puuid']
    else:
        print(f"Error al obtener PUUID: {response.status_code}, {response.text}")
        return None

def get_match_ids(puuid):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=5&api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener Match IDs: {response.status_code}, {response.text}")
        return []

def get_match_details(match_id):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        match_details = response.json()
        teams = {100: "Azul", 200: "Rojo"}
        for participant in match_details['info']['participants']:
            summoner_name = participant['summonerName']
            champion_name = participant['championName']
            team_id = participant['teamId']
            win = participant['win']
            team = teams[team_id]
            result = "Ganó" if win else "Perdió"
            print(f"Nombre: {summoner_name}, Campeón: {champion_name}, Equipo: {team}, {result}")

        # Mostrar quién ganó la partida
        winner_team = "Azul" if match_details['info']['teams'][0]['win'] else "Rojo"
        print(f"Equipo Ganador: {winner_team}")
        print()
    else:
        print(f"Error al obtener detalles del match: {response.status_code}, {response.text}")

# Solicitar nombre del jugador y tagline
game_name = input("Introduce el nombre del jugador: ")
tag_line = input("Introduce el tagline del jugador: ")

# Obtener PUUID
puuid = get_puuid(game_name, tag_line)
if puuid:
    # Obtener Match IDs
    match_ids = get_match_ids(puuid)
    if match_ids:
        # Obtener y mostrar detalles de las últimas 5 partidas
        for match_id in match_ids:
            get_match_details(match_id)
