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
        
    def has_text(self):
        return self.text() != ""
        
    def get_user(self):
        if 'user' in self.data:
            return self.data['user']

    #"user" : { "location":"San Francisco, CA" }
    def get_user_location(self):
        user = self.get_user()
        if user is not None:
            if 'location' in user:
                return user['location']

    #"place" : { "country_code":"US" }  
    def get_country_code(self):
        place = self.get_place()
        if place is not None:
            if 'country' in place:
                return place['country_code']

    #"place" : { "country_code":"US" }                
    def get_place(self):
        if 'place' in self.data:
            return self.data['place']

    def get_place_name(self):
        place = self.get_place()
        if place is not None:
            if 'full_name' in place:
                return place['full_name']
        
    def get_location(self):
        full_name = self.get_place_name()
        if full_name is not None:
            return full_name
        location = self.get_user_location()
        if location is not None:
            return location
                    
        
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


def is_state(location):
    if location is None:
        return False
    
    part = location[-4:]
    if part.startswith(',', 0,1) == False:                        
        return False

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
        
    happiness = {}
    sentiments = {} # initialize an empty dictionary

    for sentiment in sent_file:
        term, score  = sentiment.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        sentiments[term] = int(score)  # Convert the score to an integer.    
    
    for tweet in tweet_file:
        t = Tweet(json.loads(tweet))
        if t.has_text():
            score = t.score(sentiments)    
            country_code = t.get_country_code()
            if country_code != "US":
                continue
            
            location = t.get_location()    
            if is_state(location) == False:
                continue
            
            state = location[-2:]
            if state not in happiness:
                happiness[state] = 0
            
            happiness[state] += score     
              
    happiest_state = ""            
    happiest_score = 0            
    for state in happiness:
#        print state, happiness[state]
        if happiness[state] > 0:
            happiest_state = state

    print happiest_state

if __name__ == '__main__':
    main()