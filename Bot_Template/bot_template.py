import praw
import importlib
from Bot_Template import keys

importlib.import_module("keys.py")

#Text that will trigger your bot
trigger = "taskete~"
#Message your bot will post
message = "I am here!"
#If you'll post a link with your message, url is true
url = True
link = "https://gfycat.com/gifs/detail/eagerfrighteningeel"

#Reddit authentication
reddit = praw.Reddit(client_id = keys.client_id,
                     client_secret = keys.client_secret,
                     password = keys.password,
                     user_agent = "Test Script by /u/Habanero_Pepper_irl",
                     username = keys.username)

#Set the subreddit you want to go through
subreddit = reddit.subreddit("test")
submission_ids = []

#Set number of hot posts you want to go through, put their IDs in a list
for submission in subreddit.hot(limit = 1):
    submission_ids.append(submission.id)

#Go through each submission
for id in submission_ids:
    submission = reddit.submission(id)
    comments = submission.comments
    #Go through the comments of each submission
    for comment in comments:
        text = str(comment.body)
            #print(text) #in case you want to print out the comments
        if(text.lower() == trigger):
            if(url):
                comment.reply("[" + message + "](" + link + ")")
            else:
                comment.reply(message)