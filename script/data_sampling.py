import argparse
import os

import numpy as np
import pandas as pd

SCRIPT_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(SCRIPT_DIR, "..", "data")


def sample_character_dialogue(df, character_name, target_lines=300):
    np.random.seed(42)

    # Filter to the selected character
    df_character = df[df["pony"] == character_name].copy()

    if df_character.empty:
        print(f"ERROR: No dialogue found for character '{character_name}'")
        return pd.DataFrame()

    episodes = df_character["title"].unique()
    total_available = len(df_character)

    # If there are not enough lines, just return everything
    if total_available <= target_lines:
        return df_character

    samples = []

    # Proportional sampling from each episode
    for episode in episodes:
        df_episode = df_character[df_character["title"] == episode]
        n_available = len(df_episode)

        proportion = n_available / total_available
        n_sample = int(target_lines * proportion)
        n_sample = min(n_sample, n_available)

        if n_sample > 0:
            sample = df_episode.sample(n=n_sample, random_state=42)
            samples.append(sample)

    df_final = pd.concat(samples, ignore_index=True)

    # Top up if needed to reach target_lines
    if len(df_final) < target_lines:
        remaining_needed = target_lines - len(df_final)
        already_sampled = set(df_final.index)
        df_remaining = df_character[~df_character.index.isin(already_sampled)]

        if len(df_remaining) > 0:
            n_topup = min(remaining_needed, len(df_remaining))
            df_topup = df_remaining.sample(n=n_topup, random_state=42)
            df_final = pd.concat([df_final, df_topup], ignore_index=True)

    # Shuffle final result
    df_final = df_final.sample(frac=1, random_state=42).reset_index(drop=True)

    return df_final


def main():
    parser = argparse.ArgumentParser(description="Sample character dialogue")
    parser.add_argument("character_name")
    parser.add_argument("--target_lines", type=int, default=300)
    args = parser.parse_args()

    input_path = os.path.join(DATA_PATH, "mlp_s1-8.csv")
    df = pd.read_csv(input_path)

    df_sampled = sample_character_dialogue(df, args.character_name, args.target_lines)

    if df_sampled.empty:
        return

    df_sampled = df_sampled.rename(columns={"pony": "character"})

    if "writer" in df_sampled.columns:
        df_sampled = df_sampled.drop(columns=["writer"])

    output_filename = f"{args.character_name}_dialogue.csv"
    output_path = os.path.join(DATA_PATH, output_filename)
    df_sampled.to_csv(output_path, index=False)


if __name__ == "__main__":
    main()
