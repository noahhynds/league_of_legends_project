# imports
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RIOT_API_KEY")
# print("API key loaded:", bool(API_KEY))

def get_account(game_name: str, tag_line: str):
    url = (
        "https://americas.api.riotgames.com"
        f"/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    )
    response = requests.get(
        url,
        headers={"X-Riot-Token": API_KEY},
        timeout=15
    )

    return response

def get_puuid(game_name: str, tag_line: str):
    response = get_account(game_name, tag_line)
    response.raise_for_status()
    account_data = response.json()
    puuid = account_data.get("puuid")

    return puuid


def get_match_ids(puuid: str):
    url = (
        "https://americas.api.riotgames.com"
        f"/lol/match/v5/matches/by-puuid/{puuid}/ids"
        )
    response = requests.get(
        url,
        headers={"X-Riot-Token": API_KEY},
        params={"count": 100},
        timeout=15
    )
    response.raise_for_status()
    match_ids = response.json()

    return match_ids

def get_match_details(match_id: str):
    url = (
        "https://americas.api.riotgames.com"
        f"/lol/match/v5/matches/{match_id}"
        )
    response = requests.get(
        url,
        headers={"X-Riot-Token": API_KEY},
        timeout=15
    )
    response.raise_for_status()
    match_data = response.json()
    return match_data


if __name__ == "__main__":
    puuid = get_puuid("GuppyWoo", "NA1")
    match_ids = get_match_ids(puuid)

    first_match_id = match_ids[0]
    match_data = get_match_details(first_match_id)

    print("Match ID:", first_match_id)
    print("Game duration:", match_data["info"]["gameDuration"])

    
    
    
