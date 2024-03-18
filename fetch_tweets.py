from tweety import Twitter

app = Twitter("session")

def get_tweet(tweetId):
    print("Trying tweet",str(tweetId))
    tweet = app.tweet_detail(str(tweetId))
    return tweet.text