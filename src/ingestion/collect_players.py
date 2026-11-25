import pandas as pd
from pathlib import Path
import json
from src.ingestion.riot_client import (
    get_puuid,
    get_match_ids,
    get_match_details
)

file_path = Path("data/processed/player_matches.csv")

df = pd.read_csv(file_path)

unique_players = df["puuid"].unique()


all_match_ids = set()
for puuid in unique_players[:3]:
    match_ids = get_match_ids(puuid)
    all_match_ids.update(match_ids)
    print(f"Matches found: {len(match_ids)}")

print(f"Total unique matches: {len(all_match_ids)}")


output_dir = Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

for match_id in sorted(all_match_ids)[:5]:
    output_path = output_dir / f"{match_id}.json"
    if not output_path.exists():
        match_data = get_match_details(match_id)

        with open(output_path, "w") as file:
            json.dump(match_data, file, indent=4)

        print(f"Successfully saved: {match_id}")

    else:
        print(f"Match already saved: {match_id}")