import pandas as pd
from pathlib import Path


def save_collection_manifest(collection_records: list[dict]):
    output_path = Path("data/processed/player_collection_status.csv")
    temp_path = output_path.with_suffix(".tmp")

    collection_df = pd.DataFrame(collection_records)

    if output_path.exists():
        existing_df = pd.read_csv(output_path)

        collection_df = pd.concat(
            [existing_df, collection_df],
            ignore_index=True
        )

    collection_df = collection_df.drop_duplicates(
        subset=["puuid", "start_time", "end_time"],
        keep="last"
    )

    output_dir = output_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    collection_df.to_csv(temp_path, index=False)
    temp_path.replace(output_path)

    print(collection_df.to_string(index=False))
    print(f"Successfully saved: {output_path}")