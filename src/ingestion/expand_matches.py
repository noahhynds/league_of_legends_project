import pandas as pd
from pathlib import Path

from src.ingestion.riot_client import get_all_match_ids

from datetime import datetime, timezone
from src.ingestion.collection_manifest import save_collection_manifest
from src.ingestion.match_storage import (
    download_missing_matches,
    count_downloaded_matches,
    get_missing_match_ids
)

def expand_matches(player_count: int = 3,
                   match_count: int | None = None,
                   start_time: int | None = None,
                   end_time: int | None = None):
    
    file_path = Path("data/processed/player_cohort.csv")
    df = pd.read_csv(file_path)
    players = df["puuid"]

    manifest = Path("data/processed/player_collection_status.csv")
    if manifest.exists():
        manifest_df = pd.read_csv(manifest)

        completed_players = manifest_df[(manifest_df["is_complete"] == True) &
                                        (manifest_df["start_time"] == start_time) &
                                        (manifest_df["end_time"] == end_time)]["puuid"]
        players = players[~players.isin(completed_players)]
    if players.empty:
        print("All cohort players have completed collection")
        return
    print(f"Remaining players: {len(players)}")
    all_match_ids = set()
    player_match_ids = {}

    for puuid in players[:player_count]:
        match_ids = get_all_match_ids(
            puuid,
            start_time=start_time,
            end_time=end_time)
        player_match_ids[puuid] = match_ids
        all_match_ids.update(match_ids)
        print(f"Matches found: {len(match_ids)}")

    print(f"Total unique matches: {len(all_match_ids)}")

    match_ids_sorted = sorted(all_match_ids)
    missing_ids = get_missing_match_ids(match_ids_sorted)

    print(f"Missing matches: {len(missing_ids)}")

    download_missing_matches(missing_ids[:match_count])

    collection_records = []
    for puuid, match_ids in player_match_ids.items():
        expected_matches = len(match_ids)
        downloaded_matches = count_downloaded_matches(match_ids)
        is_complete = expected_matches == downloaded_matches
        record = {
        "puuid": puuid,
        "expected_matches": expected_matches,
        "downloaded_matches": downloaded_matches,
        "is_complete": is_complete,
        "start_time": start_time,
        "end_time": end_time
    }
        collection_records.append(record)

    save_collection_manifest(collection_records)

if __name__ == "__main__":
    start_time = int(datetime(2026, 9, 1, tzinfo=timezone.utc).timestamp())
    end_time = int(datetime(2026, 11, 25, tzinfo=timezone.utc).timestamp())

    expand_matches(
        player_count=3,
        match_count=50,
        start_time=start_time,
        end_time=end_time
    )