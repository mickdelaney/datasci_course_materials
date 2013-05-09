import sys
import json

class Tweet:
    def __init__(self, tweet_data):
        self.data = tweet_data

    def text(self):
        text = self.data['text'].encode('utf-8')
        return text


def main():
    sent_fie = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    sentiments = {} # initialize an empty dictionary
    for sentiment in sent_fie:
        term, score  = sentiment.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        sentiments[term] = int(score)  # Convert the score to an integer.

    count = 1
    tweets = {}
    for tweet in tweet_file:
        t = Tweet(json.loads(tweet))
        tweets[count] = t
        count += 1
        print t.text()

    print len(sentiments) # Print every (term, score) pair in the dictionary
    print len(tweets) #

if __name__ == '__main__':
    main()
