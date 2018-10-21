from WebSafetyBot import keys
from WebSafetyBot.gglsb_lookup import checkWebsite
import praw
import re
import datetime
##TO DO:
    # set subreddits bot will go through
    # make sure bot only comments once per comment in thread

regex_url = '(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+'
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
    "MALWARE": "https://media.giphy.com/media/Ab2tLKySwKI48/giphy.gif",
    #Phishing gif
    "SOCIAL ENGINEERING": "https://media1.tenor.com/images/d593b10bb25f61a76469d5b08e605b03/tenor.gif?itemid=5497478"
}

threatResponse = {
    "SAFE": "Safe! Feel free to dive in!",
    "ERROR": " Contact my programmer!",
    "MALWARE": "Malware! You definitely don't want to open this!",
    "SOCIAL ENGINEERING": "Social Engineering! You might get phished in there!"

}
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
    comments = submission.comments.list()

    #Go through the comments of each submission
    for comment in comments:
        text = str(comment.body)
        print("Comment:", text) #Print out comments for debugging
        if(trigger in text.lower()):
            #Get the comment parent id
            #Get the parent comment item
            #Get the parent comment body
            parent_txt = comment.parent()
            parent_txt = reddit.comment(id = parent_txt)
            parent_txt = str(parent_txt.body)
            #Regex to find all urls within parent text body
                #credit: GooDeeJaY answering at stackoverflow
            urls = re.findall(regex_url, parent_txt)

            #For each url, check their safety
            for url in urls:
                print("I'm running")
                response = wsb_ggsb_lookup.checkWebsite(url)
                status_code = response[0]
                threat = response[1]
                body = threatResponse[threat]
                if(threat == "ERROR"):
                    body = "ERROR: " + status_code + body
                    file = open("wsb_logs.txt", "r")
                    file.write("Date: " + datetime.date.now() + "|URL: " + url + "|Body: " + body)
                else:
                    #Formats reply to make the url a hyperlink
                    body = url + "|" + "[" + body + "](" + gifs[threat] + ")"
                message += body + "\n"
            #print("Message:",message)
            if(message != ""):
                #Build the message as a table and add a signature
                message = head + message + signature
                # print("Message")
                # print(message)
                comment.reply(message)