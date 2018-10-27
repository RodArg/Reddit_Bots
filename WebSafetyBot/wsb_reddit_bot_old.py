import keys
import wsb_ggsb_lookup
import praw
import re
import datetime

#Regex to find all urls within parent text body
                #credit: GooDeeJaY answering at stackoverflow
REGEX_URL = '(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+'

##Comment components
#Message that will trigger the bot
trigger = "!facecheck"
message = ""
#Reddit formatting for tables
head = "URL|Result \n :--|:-- \n"
#User signature bot will always show
signature = "\n" + "---" + "\n \n" + "^(I am a bot created by /u/Habanero_Pepper_irl, let him know if anything goes wrong.)"
gifs = {
    #Thumbs up gif
    "SAFE": "https://i.imgur.com/LT4GuFu.gif",
    #Robot error png
    "ERROR": "https://png2.kisspng.com/20180406/pze/kisspng-robot-safety-robotics-formassembly-computer-robot-5ac7988da99aa5.1695848615230301576947.png",
    #Sad robot gif
    "MALWARE": "https://i.pinimg.com/originals/4f/fc/97/4ffc976d9640beb49f1450b38671ec6b.gif",
    #Phishing gif
    "SOCIAL_ENGINEERING": "https://media1.tenor.com/images/d593b10bb25f61a76469d5b08e605b03/tenor.gif?itemid=5497478",
    "THREAT_TYPE_UNSPECIFIED": "https://timedotcom.files.wordpress.com/2016/10/cozmo-gif.gif",
    "UNWANTED_SOFTWARE": "https://i.pinimg.com/originals/12/8f/e5/128fe53d16665535e6bf537b0fb42139.gif",
    "POTENTIALLY_HARMFUL_APPLICATION": "https://media.giphy.com/media/Ab2tLKySwKI48/giphy.gif"
}

threatResponse = {
    "SAFE": "Safe! Feel free to dive in!",
    "ERROR": " Contact my programmer!",
    "MALWARE": "Malware! You definitely don't want to open this!",
    "SOCIAL ENGINEERING": "Social Engineering! You might get phished in there!",
    "THREAT_TYPE_UNSPECIFIED": "Threat Type Unspecified! I don't know what's here but it's bad!",
    "UNWANTED_SOFTWARE": "Unwanted Software! You won't find love here, don't go in!",
    "POTENTIALLY_HARMFUL_APPLICATION": "Potentially Harmful Application! More like, definitely harmful application!"
}

#Reddit authentication
reddit = praw.Reddit(client_id = keys.client_id,
                     client_secret = keys.client_secret,
                     password = keys.password,
                     user_agent = "WebSafetyBot by /u/Habanero_Pepper_irl",
                     username = keys.username)

sub_file = open("wsb_subreddits.txt", "r")
subreddits = []
#Number of submissions we'll check
sub_amt = 5
submission_ids = []

#Get subreddits you want to go through
for line in sub_file:
    subreddits.append(line)

sub_file.close()

#Get sub_amt hot posts you want to go through, put their IDs in a list
for sub_name in subreddits:
    subreddit = reddit.subreddit(sub_name)
    for submission in subreddit.hot(limit = sub_amt):
        submission_ids.append(submission.id)

#Get comment IDs the bot has already replied to
id_file = open("wsb_ids.txt", "a+")
comment_ids = []
id_file.seek(0)
#File format is Date, ID\n
for line in id_file:
    ids = line.split(",")
    ids = ids[1].split("\n")
    comment_ids.append(ids[0])
log_file = open("wsb_logs.txt", "a")

#Go through each submission
for id in submission_ids:
    submission = reddit.submission(id)
    comments = submission.comments.list()

    #Go through the comments of each submission
    for comment in comments:
        text = str(comment.body)
        parent_id = str(comment.parent())
        #print("Comment:", text) #Print out comments for debugging
        #print("Parent id:",parent_id)
        if(parent_id in comment_ids):
            print(parent_id, "Comment already replied to.")
        if(trigger in text.lower() and parent_id not in comment_ids):
            #Log the parent comment ID to the id_file (to make sure we don't respond to it again)
            id_file.write(str(datetime.date.today()) + "," + parent_id + "\n")
            #Get the parent comment item
            #Get the parent comment body
            parent_txt = reddit.comment(id = parent_id)
            parent_txt = str(parent_txt.body)

            urls = re.findall(REGEX_URL, parent_txt)

            #For each url, check their safety
            for url in urls:
                #print("I'm running")
                response = wsb_ggsb_lookup.checkWebsite(url)
                status_code = response[0]
                threat = response[1]
                body = threatResponse[threat]
                if(threat == "ERROR"):
                    body = "ERROR: " + status_code + body
                    log_file.write("Date: " + datetime.date.now() + "|URL: " + url + "|Body: " + body)
                else:
                    #Formats reply to make the url a hyperlink
                    body = url + "|" + "[" + body + "](" + gifs[threat] + ")"
                message += body + "\n"
            #print("Message:",message)
            log_file.close()
            if(message != ""):
                #Build the message as a table and add a signature
                message = head + message + signature
                #print("Message")
                #print(message)
                comment.reply(message)
id_file.close()