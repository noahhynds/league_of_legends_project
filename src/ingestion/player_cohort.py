import pandas as pd
from pathlib import Path


def create_player_cohort(player_count: int = 100):
    output_path = Path("data/processed/player_cohort.csv")

    if output_path.exists():
        print("Player cohort already exists. Skipping creation.")
        return
    
    file_path = Path("data/processed/player_matches.csv")

    df = pd.read_csv(file_path, parse_dates=["game_date"])

    start_date = pd.Timestamp("2026-09-01", tz="UTC")
    end_date = pd.Timestamp("2026-09-15", tz="UTC")

    df_filtered = df[(df["game_date"] >= start_date) & (df["game_date"] < end_date)].copy()

    puuid = df_filtered["puuid"].drop_duplicates()
    n_unique = len(puuid)
    print(f"Eligible players: {n_unique}")

    sample = puuid.sample(n=min(n_unique, player_count), random_state=42)
    print(f"Selected players: {len(sample)}")

    sample.to_csv(output_path, index=False)
    print(f"Successfully saved: {output_path}")


if __name__ == "__main__":
    create_player_cohort(player_count=100)