import pandas as pd
import argparse
import os
script_dir = os.path.dirname(__file__)
data_path = os.path.join(script_dir, '..', 'data')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("character_name")
    args = parser.parse_args()

    with open(os.path.join(data_path,'mlp_s1-8.csv'), 'r') as input_file:
        df = pd.read_csv(input_file)
        df_character = df[df['pony'] == args.character_name]
        # remove title column
        df_character_title = df_character.drop(columns=['title'])
        # remvove writer column
        df_character_title_writer = df_character_title.drop(columns=['writer'])
        # ramdom 350 rows
        df_character_title_writer_350 = df_character_title_writer.sample(n=350, random_state=1)

        with open(os.path.join(data_path,f'{args.character_name}_dialogue.csv'), 'w') as output_file:
            df_character_title_writer_350.to_csv(output_file, index=False)












if __name__ == "__main__":
    main()