


from collections import Counter,defaultdict
import pandas as pd
import os
import string
import math
# don't use sklearn tf-idf
script_dir = os.path.dirname(__file__)
input_data_path = os.path.join(script_dir, '..', 'data', 'data_for_analysis')
output_data_path = os.path.join(script_dir, '..', 'data')
topics = ["Friendship & Relationships" 
          , "Identity & Personal Growth" 
          , "Authority & Leadership" 
          , "History, Lore, & Magic" 
          , "Nature & Animals" 
          , "Food & Drink"]

topic_word_list = dict()
for topic in topics:
    topic_word_list[topic] = list()


def main():
    # compute the 10 words in each category/topic with highest tf-idf 
    for topic in topics:
        input_path = os.path.join(input_data_path,f"{topic}.csv")
        df = pd.read_csv(input_path)
        for line in df['dialog'].astype(str):
            for word in line.lower().split():
                word = word.strip(string.punctuation)
                if not word:
                    continue
                if len(word) < 2:
                    continue
                topic_word_list[topic].append(word)
    
    topic_tf = dict()
    for topic,words in topic_word_list.items():
        topic_tf[topic] = Counter(words)
    

    df_counts = defaultdict(int)

    for topic,tf_counter in topic_tf.items():
        for word in tf_counter.keys():
            df_counts[word] += 1

    topic_idf = dict()
    for word,df_count in df_counts.items():
        topic_idf[word] = math.log(len(topics)/df_count)

    topic_tfidf = dict()
    for topic,tf_counter in topic_tf.items():
        tfidf = dict()
        for word,tf in tf_counter.items():
            tfidf[word] = tf * topic_idf[word]
        topic_tfidf[topic] = tfidf
     # save to one csv file
    for topic,tfidf in topic_tfidf.items():
        sorted_tfidf = sorted(tfidf.items(), key=lambda x: x[1], reverse=True)
        
        top_words = sorted_tfidf[:10]
        output_path = os.path.join(output_data_path,f"top_tfidf_words.csv")
        df_output = pd.DataFrame(top_words, columns=["word","tf-idf"])
        df_output.insert(0, "topic", topic)
        if not os.path.exists(output_path):
            df_output.to_csv(output_path, index=False)
        else:
            df_output.to_csv(output_path, mode='a', header=False, index=False)
            
        

        

        






    




        


                
        
                    
            


            

            



if __name__ == "__main__":
    main()
