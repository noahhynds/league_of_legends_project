# imports
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

API_KEY = os.getenv("RIOT_API_KEY")


# helper
def riot_request(url: str, params=None):
    for i in range(5):

        time.sleep(1.3)
        response = requests.get(
            url,
            headers={"X-Riot-Token": API_KEY},
            params=params,
            timeout=15
    )
        if response.status_code == 429:
            if i == 4:
                response.raise_for_status()

            retry_after = int(response.headers.get("Retry-After", 120))

            print(f"Attempt {i + 1}. Rate limit reached. Waiting {retry_after} seconds.")
            time.sleep(retry_after)
        else:
            return response

# get account
def get_account(game_name: str, tag_line: str):
    url = (
        "https://americas.api.riotgames.com"
        f"/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    )
    response = riot_request(url)
    
    return response

# get puuid
def get_puuid(game_name: str, tag_line: str):
    response = get_account(game_name, tag_line)
    response.raise_for_status()
    account_data = response.json()
    puuid = account_data.get("puuid")

    return puuid


# get match ids
def get_match_ids(puuid: str, start: int = 0, count: int = 100):
    url = (
        "https://americas.api.riotgames.com"
        f"/lol/match/v5/matches/by-puuid/{puuid}/ids"
        )
    response = riot_request(url, params={"start": start, "count": count})
    response.raise_for_status()
    match_ids = response.json()

    return match_ids


# all matches
def get_all_match_ids(puuid: str):
    all_match_ids = []
    start = 0
    count = 100

    while True:
        match_ids = get_match_ids(puuid, start=start, count=count)
        print(f"Start: {start}, Matches retrieved: {len(match_ids)}")
        all_match_ids.extend(match_ids)

        if len(match_ids) < count:
            break

        start += count

    return all_match_ids

# get match data
def get_match_details(match_id: str):
    url = (
        "https://americas.api.riotgames.com"
        f"/lol/match/v5/matches/{match_id}"
        )
    response = riot_request(url)

    response.raise_for_status()
    match_data = response.json()
    return match_data