import pandas as pd
from pathlib import Path

from src.ingestion.riot_client import get_match_ids
from src.ingestion.match_storage import download_missing_matches

def expand_matches(player_count: int = 3, match_count: int = 50):
    file_path = Path("data/processed/player_matches.csv")

    df = pd.read_csv(file_path)

    unique_players = df["puuid"].unique()

    all_match_ids = set()

    for puuid in unique_players[:player_count]:
        match_ids = get_match_ids(puuid)
        all_match_ids.update(match_ids)
        print(f"Matches found: {len(match_ids)}")

    print(f"Total unique matches: {len(all_match_ids)}")

    download_missing_matches(sorted(all_match_ids)[:match_count])


if __name__ == "__main__":
    expand_matches()