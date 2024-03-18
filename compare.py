import json

comparisons = ['classification', 'misleadingOther', 'misleadingFactualError', 'misleadingManipulatedMedia', 'misleadingOutdatedInformation', 'misleadingUnverifiedClaimAsFact', 'misleadingSatire', 'notMisleadingOther', 'notMisleadingFactuallyCorrect', 'notMisleadingOutdatedButNotWhenWritten', 'notMisleadingClearlySatire', 'notMisleadingPersonalOpinion', 'trustworthySources']

agree_disagree = {}

for comparison in comparisons:
    agree_disagree[comparison] = {"agree": 0, "disagree": {"false negative": 0, "false positive": 0}}

# Read the data from the JSON file
with open('my_data.json') as json_file:
    data = json.load(json_file)

for tweet in data:
    for comparison in comparisons:
        if tweet["gpt"][comparison] == tweet["community_notes"][comparison]:
            agree_disagree[comparison]["agree"] += 1
        else:
            if str(tweet["gpt"][comparison]) == "0":
                agree_disagree[comparison]["disagree"]["false negative"] += 1
            else:
                agree_disagree[comparison]["disagree"]["false positive"] += 1

        
print(agree_disagree)