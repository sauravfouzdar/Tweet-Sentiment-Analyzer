import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterClient(object):
    def __init__(self):
        api_key = 'XXXXXXXXXXXXXXXXX'
        api_secret_key = 'XXXXXXXXXXXXXXXXX'
        access_token = 'XXXXXXXXXXXXXXXXX'
        access_token_secret = 'XXXXXXXXXXXXXXXXX'

        try:
            self.auth = OAuthHandler(api_key, api_secret_key)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Authentication Failed")

    def clean_tweet(self, tweet):
        # function to clean tweet by removing @, links exclamation sign etc form tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        analyzer = TextBlob(self.clean_tweet(tweet))

        '''assign sentiment   '''
        if analyzer.sentiment.polarity > 0:
            return 'Positive'
        elif analyzer.sentiment.polarity < 0:
            return 'Negative'
        else:
            return 'Neutral'

    def get_tweets(self, query, count = 10):
        tweet_list = []

        try:
            # request twitter api to fetch tweet
            fetched_tweets = self.api.search(q=query, count=count)
            for tweet in fetched_tweets:
                parse_tweet = {}
                parse_tweet['text'] = tweet.text
                parse_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                if tweet.retweet_count>0:
                    if parse_tweet not in tweet_list:
                        tweet_list.append(parse_tweet)
                else:
                    tweet_list.append(parse_tweet)

            return tweet_list
        except tweepy.TweepError as error:
            print("Error: " + str(error))


def main():
    api = TwitterClient()
    tweets = api.get_tweets(query="Rahul Gandhi", count=200)

    positive_tweets = []
    negative_tweets = []

    for tweet in tweets:
        if tweet["sentiment"] == "Positive":
            positive_tweets.append(tweet)
        elif tweet["sentiment"] == "Negative":
            negative_tweets.append(tweet)

    ''' 
    printing positive tweets
    '''
    print("Positive tweets\n")
    for tweet in positive_tweets[:5]:
        print(tweet)
    print("\n Negative tweets \n")

    for tweet in negative_tweets[:5]:
        print(tweet)


if __name__ == "__main__":
    main()

