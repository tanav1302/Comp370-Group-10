
import pandas as pd
import os
script_dir = os.path.dirname(__file__)
data_path = os.path.join(script_dir, '..', 'data')


topics = ["Friendship & Relationships" 
          , "Identity & Personal Growth" 
          , "Authority & Leadership" 
          , "History, Lore, & Magic" 
          , "Nature & Animals" 
          , "Food & Drink"]

character_names = ["Discord","Princess Celestia","Sweetie Belle"]

def main():
    df_percertage = pd.DataFrame(columns=["character","topic","percentage"])

    for character_name in character_names:
        input_path = os.path.join(data_path, f"{character_name}_for_coding - annotated.csv")
        df = pd.read_csv(input_path)
        number_dialogues = len(df)
        for topic in topics:
            # first check for null values to avoid errors
            topic_df = df[df["topic"].notnull() & df["topic"].str.contains(topic)]
            number_dialogue_topic = len(topic_df)
            percentage_topic = round(((number_dialogue_topic / number_dialogues) * 100),2)
            df_percertage = pd.concat([df_percertage, pd.DataFrame({"character":[character_name],"topic":[topic],"percentage":[percentage_topic]})], ignore_index=True)

    # save to one txt file
    output_path = os.path.join(data_path, f"topic_percentage.csv")

    df_percertage.to_csv(output_path, index=False)
    



        
        



    
    

if __name__ == "__main__":
    main()