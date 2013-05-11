#NOTES:
#Parse the tweets
#For each tweet create a score
#For each term in the tweet thats not in the sentinment file
#Add the score to that term

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
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    
    new_sentiments = {}
    
    sentiments = {} # initialize an empty dictionary
    for sentiment in sent_file:
        term, score  = sentiment.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        sentiments[term] = int(score)  # Convert the score to an integer.

    for tweet in tweet_file:
        t = Tweet(json.loads(tweet))
        score = t.score(sentiments)
        for new_term in t.new_terms(sentiments):
            if new_term not in new_sentiments:
                new_sentiments[new_term] = 0
                
            new_sentiments[new_term] += score                
#            print new_term, current_score
            
    
    for key in new_sentiments:
        print key, new_sentiments[key]

if __name__ == '__main__':
    main()
