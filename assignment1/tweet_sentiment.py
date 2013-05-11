#loop through each tweet 
#break the text into tokens
#lookup the token in the sentiment hash
#if it exists add it to the overall sentiment of the tweet, else continue to next token

import sys
import json

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


def main():
    sent_fie = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    sentiments = {} # initialize an empty dictionary
    for sentiment in sent_fie:
        term, score  = sentiment.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        sentiments[term] = int(score)  # Convert the score to an integer.

    for tweet in tweet_file:
        t = Tweet(json.loads(tweet))
        print t.score(sentiments)


if __name__ == '__main__':
    main()
