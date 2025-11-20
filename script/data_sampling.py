import pandas as pd
import argparse
import math
import os
import numpy as np

script_dir = os.path.dirname(__file__)
data_path = os.path.join(script_dir, '..', 'data')


def sample_character_dialogue(df, character_name, target_lines=300):
    np.random.seed(42)  # for reproducibility

    df_character = df[df["pony"] == character_name].copy()

    if df_character.empty:
        print(f"ERROR: No dialogue found for '{character_name}'")
        return pd.DataFrame()

    episodes = df_character["title"].unique()
    total_available = len(df_character)

    print(f"Found {total_available} lines across {len(episodes)} episodes")

    if total_available <= target_lines:
        return df_character

    samples = []

    # sample from each episode proportionally
    for episode in episodes:
        df_episode = df_character[df_character["title"] == episode]
        n_available = len(df_episode)

        proportion = n_available / total_available
        n_sample = math.ceil(target_lines * proportion)  # round up to get 300+
        n_sample = min(n_sample, n_available)  # can't sample more than available

        if n_sample > 0:
            sample = df_episode.sample(n=n_sample, random_state=42)
            samples.append(sample)

    df_final = pd.concat(samples, ignore_index=True)
    df_final = df_final.sort_values(['title']).reset_index(drop=True)  # sort by episode

    print(f"Sampled {len(df_final)} lines")

    return df_final


def prepare_for_coding(df_sampled):
    # add line_id for reference
    df_sampled['line_id'] = range(1, len(df_sampled) + 1)

    # empty columns for manual coding
    df_sampled['topic'] = ''
    df_sampled['notes'] = ''

    coding_columns = ['line_id', 'character', 'title', 'dialog', 'topic', 'notes']

    existing_columns = [col for col in coding_columns if col in df_sampled.columns]
    df_sampled = df_sampled[existing_columns]

    return df_sampled


def create_context_lookup(df_original, character_name, output_path):
    # create reference file with context
    df_character = df_original[df_original["pony"] == character_name].copy()
    df_character = df_character.sort_values(['title']).reset_index(drop=True)

    # add previous and next dialogue
    df_character['prev_pony'] = df_character.groupby('title')['pony'].shift(1).fillna('')
    df_character['prev_dialog'] = df_character.groupby('title')['dialog'].shift(1).fillna('')
    df_character['next_pony'] = df_character.groupby('title')['pony'].shift(-1).fillna('')
    df_character['next_dialog'] = df_character.groupby('title')['dialog'].shift(-1).fillna('')

    df_character['line_id'] = range(1, len(df_character) + 1)

    context_columns = ['line_id', 'title', 'pony', 'prev_pony', 'prev_dialog',
                      'dialog', 'next_pony', 'next_dialog']

    df_context = df_character[context_columns]
    df_context.to_csv(output_path, index=False)

    return df_context


def main():
    parser = argparse.ArgumentParser(description="Sample character dialogue")
    parser.add_argument("character_name", help="Character name to sample")
    parser.add_argument("--target_lines", type=int, default=300,
                       help="Target number of lines (default: 300)")
    parser.add_argument("--open_coding_size", type=int, default=100,
                       help="Number of lines for open coding (default: 100)")
    args = parser.parse_args()

    input_path = os.path.join(data_path, "mlp_s1-8.csv")
    df = pd.read_csv(input_path)

    df_sampled = sample_character_dialogue(df, args.character_name, args.target_lines)

    if df_sampled.empty:
        return

    df_sampled = df_sampled.rename(columns={"pony": "character"})

    if "writer" in df_sampled.columns:
        df_sampled = df_sampled.drop(columns=["writer"])

    df_sampled = prepare_for_coding(df_sampled)

    # save main file
    output_filename = f"{args.character_name}_for_coding.csv"
    output_path = os.path.join(data_path, output_filename)
    df_sampled.to_csv(output_path, index=False)
    print(f"Saved {len(df_sampled)} lines to {output_filename}")

    # save subset for open coding
    df_open_coding = df_sampled.head(args.open_coding_size)
    open_coding_filename = f"{args.character_name}_open_coding_{args.open_coding_size}.csv"
    open_coding_path = os.path.join(data_path, open_coding_filename)
    df_open_coding.to_csv(open_coding_path, index=False)
    print(f"Saved first {args.open_coding_size} lines to {open_coding_filename}")

    # save context lookup
    context_filename = f"{args.character_name}_context_lookup.csv"
    context_path = os.path.join(data_path, context_filename)
    create_context_lookup(df, args.character_name, context_path)
    print(f"Saved context lookup to {context_filename}")


if __name__ == "__main__":
    main()