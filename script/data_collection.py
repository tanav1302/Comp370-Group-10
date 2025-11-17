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
        # change colmn name pony to character
        df = df.rename(columns={'pony': 'side character'})
        df_character = df[df['side character'] == args.character_name]

        # get number of unique titles
        unique_titles = df_character['title'].nunique() 
        # list of unique titles
        unique_titles_list = df_character['title'].unique().tolist()
        

        lines_per_title = 350 / unique_titles
        df_character_350= pd.DataFrame()
        

        for title in unique_titles_list:
            df_title = df_character[df_character['title'] == title]
            # get top lines_per_title rows
            df_title_top = df_title.head(min(int(lines_per_title),len(df_title)))

            df_character_350 = pd.concat([df_character_350, df_title_top], ignore_index=True)   


        df_character_350 = df_character_350.drop(columns=['writer'])

        with open(os.path.join(data_path,f'{args.character_name}_dialogue.csv'), 'w') as output_file:
            df_character_350.to_csv(output_file, index=False)






if __name__ == "__main__":
    main()