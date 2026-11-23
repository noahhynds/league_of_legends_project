# imports
import json
from pathlib import Path
import pandas as pd



raw_dir = Path("data/raw")


match_records = []

for file_path in raw_dir.glob("*.json"):
    with open(file_path, "r") as file:
        match_data = json.load(file)
    match_id = match_data["metadata"]["matchId"]
    game_creation = match_data["info"]["gameCreation"]
    game_duration = match_data["info"]["gameDuration"]
    game_date = pd.to_datetime(game_creation, unit="ms", utc=True)
    participants = match_data["info"]["participants"]
    game_mode = match_data["info"]["gameMode"]
    game_version = match_data["info"]["gameVersion"]
    queue_id = match_data["info"]["queueId"]

    for participant in participants:
        puuid = participant["puuid"]
        kills = participant["kills"]
        win = participant["win"]
        champion_name = participant["championName"]
        time_played = participant["timePlayed"]
        deaths = participant["deaths"]
        assists = participant["assists"]
        champ_level = participant["champLevel"]
        team_position = participant["teamPosition"]
        game_ended_early_surrender = participant["gameEndedInEarlySurrender"]
        game_ended_surrender = participant["gameEndedInSurrender"]
        summoner_level = participant["summonerLevel"]
        team_early_surrender = participant["teamEarlySurrendered"]


        match_record = {
            # match information
            "match_id": match_id,
            "game_date": game_date,
            "game_duration": game_duration,
            "game_mode": game_mode,
            "game_version": game_version,
            "queue_id": queue_id,

            # player information
            "puuid": puuid,
            "summoner_level": summoner_level,
            "champion_name": champion_name,
            "champ_level": champ_level,
            "team_position": team_position,

            # performance information
            "win": win,
            "kills": kills,
            "deaths": deaths,
            "assists": assists,
            "time_played": time_played,

            # surrender information
            "game_ended_early_surrender": game_ended_early_surrender,
            "game_ended_surrender": game_ended_surrender,
            "team_early_surrender": team_early_surrender
        }
        match_records.append(match_record)


df = pd.DataFrame(match_records)
print(df)
print(df.shape)
print(df.dtypes)
print(df.isna().sum())
print(df.duplicated(subset=["match_id", "puuid"]).sum())

output_dir = Path("data/processed")

output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / "player_matches.csv"

df.to_csv(output_path, index=False)

print(f"Successfully saved: {output_path}")