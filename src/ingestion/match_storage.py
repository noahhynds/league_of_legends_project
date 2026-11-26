# imports
import json
from pathlib import Path
from src.ingestion.riot_client import get_match_details


def save_match(match_id: str, match_data: dict):
    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{match_id}.json"

    with open(output_path, "w") as file:
        json.dump(match_data, file, indent=4)


def download_missing_matches(match_ids: list[str]):
    output_dir = Path("data/raw")

    for match_id in match_ids:
        output_path = output_dir / f"{match_id}.json"
        if not output_path.exists():
            match_data = get_match_details(match_id)
            save_match(match_id, match_data)
            print(f"Successfully saved: {match_id}")
        else:
            print(f"Match already saved: {match_id}")




def count_downloaded_matches(match_ids: list[str]):
    output_dir = Path("data/raw")
    downloaded_count = 0

    for match_id in match_ids:
        output_path = output_dir / f"{match_id}.json"

        if output_path.exists():
            downloaded_count += 1

    return downloaded_count


def get_missing_match_ids(match_ids: list[str]):
    output_dir = Path("data/raw")
    missing_match_ids = []

    for match_id in match_ids:
        output_path = output_dir / f"{match_id}.json"
        
        if not output_path.exists():
            missing_match_ids.append(match_id)
    
    return missing_match_ids