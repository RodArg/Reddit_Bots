import praw
from praw.models import MoreComments
import datetime
import re

##Subreddit functions
def getSubreddits(subreddits_list):
    subreddits = []
    for subreddit in subreddits_list:
        subreddits.append(subreddit)
    return subreddits

def getSubredditsFromFile(filename):
    sub_file = open(filename, "r") # File format is: subreddit \n subreddit \n ...
    subreddits = []
    for line in sub_file:
        subreddits.append(line)
    #sub_file.close()
    return subreddits

def getSubmissions(reddit, subreddits, sub_amt):
    submissions = []
    for sub_name in subreddits:
        subreddit = reddit.subreddit(sub_name)
        for submission in subreddit.hot(limit=sub_amt):
            submissions.append(submission.id)
    return submissions

def buildHyperlink(text, link):
    return "[" + text + "](" + link + ")"

##Replied to ID functions
def getRepliedToIDs(filename):
    id_file = open(filename, "r") #File format is: DATE, comment_ID \n DATE, comment_ID \n ...
    replied_to = []
    id_file.seek(0)
    for line in id_file:
        ids = line.split(",")  # ->["DATE", "comment_ID\n"]
        if(len(ids) > 1): #will be true if file is not empty
            ids = ids[1].split("\n")  # ->["comment_ID", ""]
            replied_to.append(ids[0])
    id_file.close()
    return replied_to

def bufferResponseID(id):
    return str(datetime.date.today()) + "," + id + "\n"

def logResponseID(filename, id_buffer):
    id_file = open(filename, "a")
    id_file.write(id_buffer)
    print("Wrote to IDs file")
    #id_file.close()


##Error functions
def bufferError(errorString):
    return "Date: " + str(datetime.date.now()) + errorString

def logError(filename, err_buffer):
    log_file = open(filename, "a")
    log_file.write(err_buffer)
    #log_file.close()

##Find comment ID function
#returns a list of comment IDs that matched the trigger
def findCommentID(reddit,submission_ids, trigger):
    target_comments = []
    for id in submission_ids:
        submission = reddit.submission(id)
        submission.comments.replace_more(limit=0) #removes 'Load More Comments' #change 0 to None to load all comments per submission
        comments = submission.comments.list()  # Flat list of submission comments
        for comment in comments:
            text = str(comment.body)
            print("Comment text:", text)
            if (trigger in text.lower()):
                target_comments.append(comment)
    if(len(target_comments) > 0):
        return target_comments
    return False

def findParentID(reddit, trigger):
    for id in submission_ids:
        submission = reddit.submission(id)
        comments = submission.comments.list()  # Flat list of submission comments
        for comment in comments:
            text = str(comment.body)
            parent_id = str(comment.parent())
            if (trigger in text.lower()):
                # Log the parent comment ID to the id_file (to make sure we don't respond to it again)
                return parent_id
    return False

def haveRepliedTo(comment, replied_to):
    if(comment in replied_to):
        return True
    return False

def unlinkURL(url):
    url = re.sub(r'(https?://)',r'', url)
    url = re.sub(r'(www.)(?!com)',r'',url)
    return url
