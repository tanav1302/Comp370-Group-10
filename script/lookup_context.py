import pandas as pd
import argparse
import os

script_dir = os.path.dirname(__file__)
data_path = os.path.join(script_dir, '..', 'data')


def lookup_line(character_name, line_id):
    context_file = os.path.join(data_path, f"{character_name}_context_lookup.csv")

    if not os.path.exists(context_file):
        print(f"ERROR: Context file not found: {context_file}")
        return

    df = pd.read_csv(context_file)

    if line_id not in df['line_id'].values:
        print(f"ERROR: Line {line_id} not found (available: 1-{len(df)})")
        return

    line = df[df['line_id'] == line_id].iloc[0]

    print(f"\nLine {line_id} - {line['title']}")

    if line['prev_pony']:
        print(f"\nPrevious ({line['prev_pony']}):")
        print(f"{line['prev_dialog']}")

    print(f"\nCurrent ({line['pony']}):")
    print(f"{line['dialog']}")

    if line['next_pony']:
        print(f"\nNext ({line['next_pony']}):")
        print(f"{line['next_dialog']}")


def show_range(character_name, start_id, end_id):
    context_file = os.path.join(data_path, f"{character_name}_context_lookup.csv")

    if not os.path.exists(context_file):
        print(f"ERROR: Context file not found: {context_file}")
        return

    df = pd.read_csv(context_file)

    lines = df[(df['line_id'] >= start_id) & (df['line_id'] <= end_id)]

    if lines.empty:
        print(f"ERROR: No lines found in range {start_id}-{end_id}")
        return

    print(f"\nLines {start_id}-{end_id} for {character_name}")

    for _, line in lines.iterrows():
        print(f"\n[{line['line_id']}] {line['title']}")
        if line['prev_pony']:
            print(f"Previous ({line['prev_pony']}): {line['prev_dialog'][:60]}...")
        print(f"Current ({line['pony']}): {line['dialog']}")
        if line['next_pony']:
            print(f"Next ({line['next_pony']}): {line['next_dialog'][:60]}...")


def main():
    parser = argparse.ArgumentParser(description="Look up context for dialogue lines")
    parser.add_argument("character_name", help="Character name")
    parser.add_argument("line_id", type=int, help="Line ID to look up")
    parser.add_argument("end_id", type=int, nargs='?', help="Optional end of range")

    args = parser.parse_args()
    
    if args.end_id:
        show_range(args.character_name, args.line_id, args.end_id)
    else:
        lookup_line(args.character_name, args.line_id)


if __name__ == "__main__":
    main()