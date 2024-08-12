from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

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
        return None

def get_match_ids(puuid):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=5&api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def get_match_details(match_id):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        match_details = response.json()
        teams = {100: "Azul", 200: "Rojo"}
        team_data = {100: [], 200: []}

        for participant in match_details['info']['participants']:
            summoner_name = participant['summonerName'] or "Desconocido"
            champion_name = participant['championName']
            team_id = participant['teamId']
            win = participant['win']
            result = "Ganó" if win else "Perdió"
            kills = participant['kills']
            deaths = participant['deaths']
            assists = participant['assists']
            team_data[team_id].append({
                "summoner_name": summoner_name,
                "champion_name": champion_name,
                "kills": kills,
                "deaths": deaths,
                "assists": assists,
                "result": result
            })

        match_result = {
            "teams": {
                "Azul": team_data[100],
                "Rojo": team_data[200]
            },
            "winner": "Azul" if match_details['info']['teams'][0]['win'] else "Rojo"
        }
        return match_result
    else:
        return None

@app.route('/Partidas/<string:game_name>/<string:tag_line>', methods=['GET'])
def partidas(game_name, tag_line):
    puuid = get_puuid(game_name, tag_line)
    if puuid:
        match_ids = get_match_ids(puuid)
        results = {}
        for i, match_id in enumerate(match_ids, start=1):
            match_details = get_match_details(match_id)
            if match_details:
                results[f"Match_id{i}"] = match_details
        return jsonify(results)
    else:
        return jsonify({"error": "No se encontró el PUUID"}), 404

if __name__ == '__main__':
    app.run(debug=True)
