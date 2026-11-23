# imports
import json
from pathlib import Path

from src.ingestion.riot_client import (
    get_puuid,
    get_match_ids,
    get_match_details
)

# collect all matches
def collect_matches(game_name: str, tag_line: str, count: int = 5):
    puuid = get_puuid(game_name, tag_line)
    match_ids = get_match_ids(puuid)

    if len(match_ids) == 0:
        print("No matches yet")
        return


    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for match_id in match_ids[:count]:
        output_path = output_dir / f"{match_id}.json"

        if not output_path.exists():
            match_data = get_match_details(match_id)
            with open(output_path, "w") as file:
                json.dump(match_data, file, indent=4)
            print(f"Successfully saved: {match_id}")
        else:
            print(f"Match already saved: {match_id}")
