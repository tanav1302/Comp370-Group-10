import pandas as pd
import os
script_dir = os.path.dirname(__file__)
data_path = os.path.join(script_dir, '..', 'data')
output_data_path = os.path.join(data_path, 'data_for_analysis')

topics = ["Friendship & Relationships" 
          , "Identity & Personal Growth" 
          , "Authority & Leadership" 
          , "History, Lore, & Magic" 
          , "Nature & Animals" 
          , "Food & Drink"]

character_names = ["Discord","Princess Celestia","Sweetie Belle"]

def main():
    # make a csv for each topic containing all dialogues related to that
    for topic in topics:
        topic_df = pd.DataFrame(columns=["line_id","character","dialog","title"])
        for character_name in character_names:
            input_path = os.path.join(data_path, f"{character_name}_for_coding - annotated.csv")
            df = pd.read_csv(input_path)
            # first check for null values to avoid errors
            character_topic_df = df[df["topic"].notnull() & df["topic"].str.contains(topic)]
            topic_df = pd.concat([topic_df, character_topic_df[["line_id","character","dialog","title"]]], ignore_index=True)
        output_path = os.path.join(output_data_path,f"{topic}.csv")
        topic_df.to_csv(output_path, index=False)
            

            



if __name__ == "__main__":
    main()