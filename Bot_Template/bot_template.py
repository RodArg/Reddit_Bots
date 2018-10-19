import praw
import importlib
from Bot_Template import keys

importlib.import_module("keys.py")

#Text that will trigger your bot
trigger = "I am testing my bot! Don't mind me."
#Message your bot will post
message = "I am here!"
#If you'll post a link with your message, hyperlink is true
hyperlink = True
url = "<url you want your bot to post>"

#Reddit authentication
reddit = praw.Reddit(client_id = keys.client_id,
                     client_secret = keys.client_secret,
                     password = keys.password,
                     user_agent = "Test Script by /u/Your Reddit Username",
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
            if(hyperlink):
                comment.reply("[" + message + "](" + url + ")")
            else:
                comment.reply(message)
