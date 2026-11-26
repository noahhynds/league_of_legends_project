# imports
from src.ingestion.riot_client import (
    get_puuid,
    get_match_ids,
)
from src.ingestion.match_storage import download_missing_matches

# collect all matches
def collect_seed_matches(game_name: str, tag_line: str, count: int = 5):
    puuid = get_puuid(game_name, tag_line)
    match_ids = get_match_ids(puuid)

    if len(match_ids) == 0:
        print("No matches yet")
        return

    download_missing_matches(match_ids[:count])


if __name__ == "__main__":
    collect_seed_matches("GuppyWoo", "NA1", count=5)