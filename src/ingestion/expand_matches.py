import pandas as pd
from pathlib import Path

from src.ingestion.riot_client import get_all_match_ids

from datetime import datetime, timezone

from src.ingestion.match_storage import (
    download_missing_matches,
    count_downloaded_matches,
    get_missing_match_ids
)

def expand_matches(player_count: int = 3,
                   match_count: int | None = None,
                   start_time: int | None = None,
                   end_time: int | None = None):
    file_path = Path("data/processed/player_matches.csv")

    df = pd.read_csv(file_path)

    unique_players = df["puuid"].unique()

    all_match_ids = set()
    player_match_ids = {}

    for puuid in unique_players[:player_count]:
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

    collection_df = pd.DataFrame(collection_records)
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "player_collection_status.csv"

    collection_df.to_csv(output_path, index=False)
    print(collection_df)
    print(f"Successfully saved: {output_path}")

if __name__ == "__main__":
    start_time = int(datetime(2026, 9, 1, tzinfo=timezone.utc).timestamp())
    end_time = int(datetime(2026, 11, 25, tzinfo=timezone.utc).timestamp())

    expand_matches(
        player_count=3,
        match_count=50,
        start_time=start_time,
        end_time=end_time
    )