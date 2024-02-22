# filter for keywords from keywords.txt
import pandas as pd

def read_words_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            words = file.readlines()
            # Stripping newline characters from each word
            words = [word.strip().lower() for word in words]
            return words
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []
    

# check for each keyword in tweet text, case insensitive as well
def check_for_keywords(text, keywords, exclusions) -> tuple[bool, str]:
   # lowercase text 
    lower_text = text.lower()
    # print(lower_text)
    for keyword in keywords:
        if(keyword in lower_text):
            index = lower_text.find(keyword)
            # make sure this text exlcudes certain words
            exclude_word_found = False
            for exclude in exclusions:
                if(exclude in lower_text):
                    exclude_word_found = True
                    break
            
            if(not exclude_word_found):
                return (True, keyword)

    return (False, '')
    
if(__name__ == '__main__'):
    keywords = read_words_from_file('keywords.txt')
    exclusions = read_words_from_file('exclude.txt')
    tweets = pd.read_csv('combined_travis_tweets.csv')
    tweets['contains_keyword'] = tweets.apply(lambda row: check_for_keywords(str(row['tweet_text']), keywords, exclusions)[0], axis=1)
    tweets['keyword'] = tweets.apply(lambda row: check_for_keywords(str(row['tweet_text']), keywords, exclusions)[1], axis=1)

    tweets = tweets[tweets['contains_keyword']]
    print(len(tweets))

    tweet_text_only = tweets[["tweet_text", "keyword"]]
    tweets.to_csv('manual_filtered_travis_tweets.csv')
    tweet_text_only.to_csv('tt_manual_filtered_travis_tweets.csv')
    