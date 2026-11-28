from datetime import datetime, timezone
from src.ingestion.expand_matches import expand_matches


def collect_cohort():
    start_time = int(datetime(2026, 9, 1, tzinfo=timezone.utc).timestamp())
    end_time = int(datetime(2026, 11, 25, tzinfo=timezone.utc).timestamp())
    batch_number = 1
    try:
        while True:
            print(f"Batch {batch_number}")
            is_complete = expand_matches(player_count=3, match_count=50, start_time=start_time, end_time=end_time)
            if is_complete:
                break

            batch_number += 1
    except KeyboardInterrupt:
        print("Collection Interrupted")



if __name__ == "__main__":
    collect_cohort()