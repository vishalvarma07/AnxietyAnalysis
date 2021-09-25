# #Importing required packages
import praw
import pandas as pd
from datetime import datetime
import re

# PRAW(Python reddit Api Wrapper),Gaining developer access to reddit api and providing details for scraping.
# Using a dummy reddit account
reddit = praw.Reddit("bot1", user_agent="u/bot2user")

# #The subreddit that has to be scraped
sub = ['Anxiety']

# #Scraping the latest 500 subreddits
subreddit = reddit.subreddit(sub[0]).new(limit=500)

# #function to convert unix time to utc


def unix_to_utc(unix):
    unix_time = int(unix)
    return datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d')


# #I really could not classify a particular submission as anxious or not.
# #While I was looking through a few submissions on reddit, i figured out a pattern between flair and anxiousness
# # MOST of the submissions with these flairs had non-anxious data.
non_anxiety_flair_list = ['Discussion', 'Uplifting', 'Recovery Story', 'Progress!', 'DAE Questions']

# #subreddit info
subreddit_info = {
    "title": [],
    "score": [],
    "id": [],
    "flairs": [],
    "url": [],
    "n_comments": [],
    "created": [],
    "body": [],
    "anxious": []
}

# #Iterating over the scraped submission to store in the dictionary created
for item in subreddit:
    subreddit_info["title"].append(re.sub('[^a-zA-Z]', ' ', item.title))
    subreddit_info["score"].append(item.score)
    subreddit_info["id"].append(item.id)
    subreddit_info['flairs'].append(item.link_flair_text)
    subreddit_info["url"].append(item.url)
    subreddit_info["n_comments"].append(item.num_comments)
    subreddit_info["created"].append(unix_to_utc(item.created))
    subreddit_info["body"].append(re.sub('[^a-zA-Z]', ' ', item.selftext))
    if item.link_flair_text not in non_anxiety_flair_list:  # Classifying submissions based on the flairs
        subreddit_info["anxious"].append(1)
    else:
        subreddit_info["anxious"].append(0)


# #Creating the dataFrame/CSV/Database
make_df = pd.DataFrame(subreddit_info)
make_df.to_csv("subreddit.csv")

