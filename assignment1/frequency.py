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

    term_count = 0.0
    occurrences = {}
    
    for tweet in tweet_file:
        t = Tweet(json.loads(tweet))
        for term in t.tokens():
            term_count += 1
            if term not in occurrences:
                occurrences[term] = 0
            occurrences[term] += 1                            

    for term in occurrences:
        print term, occurrences[term]/term_count
        


if __name__ == '__main__':
    main()
