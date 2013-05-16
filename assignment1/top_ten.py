#NOTES:
# of occurrences of the term in all tweets 
# hash [term, term_count]
# of occurrences of all terms in all tweets
# term_count

import sys
import json
from collections import defaultdict


class Tweet:
    def __init__(self, tweet_data):
        self.data = tweet_data

    #Extract the text field from the raw data
    def text(self):
        text = ""
        if 'text' in self.data:
            text = self.data['text'].encode('utf-8')
        return text
    
    #Split the text into tokens
    def tokens(self):
        return self.text().split()


    #"entities":
    #{
    #    "hashtags":[],
    #    "urls":[],
    #    "user_mentions":[]
    #}
    def entities(self):
        if 'entities' in self.data:
            return self.data['entities']
            
    def hash_tags(self):
        return self.data.get('entities', {}).get('hashtags')
        entities = self.entities()
        if entities is not None:
            return entities['hashtags']
        
    #aggregate for each token
    #sentiment value or 0
    def score(self, sentiments):
        sentiment_score = 0
        for token in self.tokens():
            if token in sentiments:
                sentiment_score += sentiments[token]        
        return sentiment_score    

    def new_terms(self, sentiments):
        for token in self.tokens():
            if token not in sentiments:
                yield token

def main():
    tweet_file = open(sys.argv[1])
    
    hash_tags = {}
    
    for tweet in tweet_file:
        t = Tweet(json.loads(tweet))    
    
        for hash_tag in t.hash_tags():
            for d in hash_tag:
                print d, type(d)
            
#            if hash_tag not in hash_tags:
#               hash_tags[hash_tag] = 0
#            hash_tags[hash_tag] += 1     

    for hash_tag in hash_tags:
        print hash_tag, hash_tags[hash_tag]
    
if __name__ == '__main__':
    main()
    