# Helpful source: https://conspirator0.substack.com/p/fun-with-community-notes-data
import pandas as pd
from langdetect import detect
from fetch_tweets import get_tweet
import json
from time import sleep

N = 100 # number of tweets to gather in this experiment

# get the notes
notes = pd.read_csv("notes-00000.tsv", sep="\t")
notes["t"] = pd.to_datetime(notes["createdAtMillis"], unit="ms")
print("total notes: " + str(len(notes.index)))

# get notes status
history = pd.read_csv("noteStatusHistory-00000.tsv", sep="\t")
history = history.loc[:, history.columns.intersection(['noteId','currentStatus'])]

# merge on noteId
df = notes.merge(history, on="noteId")
print("notes with status values: " + str(len(df.index)))

# print a summary table of current note statuses
g = df.groupby("currentStatus")
summary = pd.DataFrame({"count" : g.size()}).reset_index()
print(summary)
print()

# limit to notes currently shown on posts
helpful_notes = df[df["currentStatus"] == "CURRENTLY_RATED_HELPFUL"]
print("visible notes: " + str(len(helpful_notes.index)))
print("posts with notes: " + str(len(set(helpful_notes["tweetId"]))))
print()

# get rid of non media notes
non_media_helpful = helpful_notes[helpful_notes["isMediaNote"] == 0]
print("visible note notes on non-media: " + str(len(non_media_helpful.index)))
print("non-media posts with notes: " + str(len(set(non_media_helpful["tweetId"]))))
print()


# drop helpful notes that or on the same tweet, keeping only one helpful note
non_media_helpful = non_media_helpful.drop_duplicates(subset=['tweetId'])
assert(len(non_media_helpful.index) == len(set(non_media_helpful["tweetId"])))


# drop everything I don't want
non_media_helpful = non_media_helpful.drop(columns=['noteAuthorParticipantId', 'createdAtMillis', 'believable', 'harmful', 'validationDifficulty', 'currentStatus', 'isMediaNote', 't'])


tweets_and_notes = []

for i, row in non_media_helpful.iterrows():

    if len(tweets_and_notes) == N:
        break

    row_dict = row.to_dict()

    if detect(row_dict['summary']) == 'en': # summary is in english
        # then we want to fetch the tweet
        try:
            tweet_text = get_tweet(row_dict['tweetId'])
        except Exception as e:
            sleep(6)
            continue
        sleep(6)
        if "twitter.com" not in tweet_text and "t.co" not in tweet_text:
            tweets_and_notes.append({"text": tweet_text, "community_notes": row_dict})
            # Write to JSON file after every update
            with open('tweets_and_notes_backup.json', 'w') as file:
                json.dump(tweets_and_notes, file)
                print("got another tweet")
        else:
            print("tweet discarded")
