import requests

api_key = 'RGAPI-4a1c3d23-1048-4875-939d-88787fbea1e2'
game_name = 'Jos5YT'
tag_line = 'LAN'

url = f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}?api_key={api_key}'

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "es-419,es;q=0.9,es-ES;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    account_info = response.json()
    puuid = account_info['puuid']
    print(f"PUUID: {puuid}")
else:
    print(f"Error: {response.status_code}, {response.text}")
import requests

# Reemplaza estos valores con los correctos
puuid = "dXDYEK2cfCrMqX88JDbvZLiIS9ZcE7bFRcGJ5i5UCHnbHYEiMVuSAjWdk8zWlbyG4rIy5gciIMPXKA"
region = "americas"

url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20&api_key={api_key}"

response = requests.get(url)

if response.status_code == 200:
    match_ids = response.json()
    print("Match IDs:", match_ids)
else:
    print("Error:", response.status_code, response.text)
  # Usa uno de los match IDs obtenidos

region = "americas"
match_id = "LA1_1546178787"  # Usa uno de los match IDs obtenidos

# URL para obtener los detalles del match
url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}"

response = requests.get(url)

if response.status_code == 200:
    match_details = response.json()

    # Extraer la información relevante
    for participant in match_details['info']['participants']:
        summoner_name = participant['summonerName']
        champion_name = participant['championName']
        summoner_id = participant['summonerId']
        puuid = participant['puuid']
        team_id = participant['teamId']
        
        team = "Azul" if team_id == 100 else "Rojo"

        print(f"Summoner Name: {summoner_name}, Champion: {champion_name}, Team: {team}, Summoner ID: {summoner_id}, PUUID: {puuid}")
else:
    print("Error:", response.status_code, response.text)