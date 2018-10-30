import keys
import wsb_ggsb_lookup
import wsb_reddit_functions as rf
import praw
import re
import time

##To Do:
    #Make it so user chooses whether bot checks all comments on all of reddit or only does so in certain subreddits
LOG_FILE = "wsb_logs.txt"
RESPONDED_TO_FILE = "wsb_ids.txt"
SUBREDDITS_FILE = "wsb_subreddits.txt"

#Regex to find all urls within parent text body #credit: GooDeeJaY answering at stackoverflow
REGEX_URL = '(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+'

trigger = "!facecheck"

head = "URL|Result (GIFs) \n :--|:-- \n" #Reddit formatting for tables
signature = "\n" + "---" + "\n \n" + "^(I am a bot created by /u/Habanero_Pepper_irl, let him know if anything goes wrong.)"
gifs = {
    #Thumbs up gif
    "SAFE": "https://i.imgur.com/LT4GuFu.gif",
    #Robot error png
    "ERROR": "https://png2.kisspng.com/20180406/pze/kisspng-robot-safety-robotics-formassembly-computer-robot-5ac7988da99aa5.1695848615230301576947.png",
    #Evil robot gif
    "MALWARE": "https://i.pinimg.com/originals/4f/fc/97/4ffc976d9640beb49f1450b38671ec6b.gif",
    #Phishing gif
    "SOCIAL_ENGINEERING": "https://media1.tenor.com/images/d593b10bb25f61a76469d5b08e605b03/tenor.gif?itemid=5497478",
    #Robot table flip gif
    "THREAT_TYPE_UNSPECIFIED": "https://timedotcom.files.wordpress.com/2016/10/cozmo-gif.gif",
    #Robot goalie fail gif
    "UNWANTED_SOFTWARE": "https://i.pinimg.com/originals/12/8f/e5/128fe53d16665535e6bf537b0fb42139.gif",
    #Sad robot gif
    "POTENTIALLY_HARMFUL_APPLICATION": "https://media.giphy.com/media/Ab2tLKySwKI48/giphy.gif"
}
threatResponse = {
    "SAFE": "Safe! Feel free to dive in!",
    "ERROR": " Contact my programmer!",
    "MALWARE": "Malware! You definitely don't want to open this!",
    "SOCIAL_ENGINEERING": "Social Engineering! You might get phished in there!",
    "THREAT_TYPE_UNSPECIFIED": "Threat Type Unspecified! I don't know what's here but it's bad!",
    "UNWANTED_SOFTWARE": "Unwanted Software! You won't find love here, don't go in!",
    "POTENTIALLY_HARMFUL_APPLICATION": "Potentially Harmful Application! More like, definitely harmful application!"
}

reddit = praw.Reddit(client_id = keys.client_id,
                     client_secret = keys.client_secret,
                     password = keys.password,
                     user_agent = "WebSafetyBot by /u/Habanero_Pepper_irl",
                     username = keys.username)

subreddits = rf.getSubredditsFromFile(SUBREDDITS_FILE) #will be a list

def checkURLSafety(urls):
    responses = []
    for url in urls:
        response = wsb_ggsb_lookup.checkWebsite(url)
        status_code = response[0]
        threat = response[1]
        url = rf.unlinkURL(url)  # Makes any url not a link
        if (threat == "ERROR"):
            print(status_code + threatResponse[threat], url)
        responses.append([url, threat])
    return responses

def buildReply(responses):
    reply = ""
    for response in responses:
        url = response[0]
        threat = response[1]
        reply += url + "|" + rf.buildHyperlink(threatResponse[threat], gifs[threat]) + "\n"
    return reply

def searchComments(comments):
    id_buffer = ""
    err_buffer = ""
    count = 0
    while(True):
        try:
            print("Executing WSB")
            reply = ""
            responded_to_ids = rf.getRepliedToIDs(RESPONDED_TO_FILE)
            for comment in comments:
                print(count,"/u/", comment.author, "Comment:", comment.body)
                count += 1 #for debugging
                if (comment.id not in responded_to_ids and trigger in comment.body.lower()):
                    id_buffer += rf.bufferRespondedToID(comment.id)
                    parent_comment = reddit.comment(id=comment.parent()).body
                    urls = re.findall(REGEX_URL, parent_comment)
                    responses = checkURLSafety(urls)
                    if (urls != ""):
                        reply = buildReply(responses)
                        reply = head + reply + signature
                        print("Printing Message:", reply)
                        comment.reply(reply)
                        time.sleep(2)
        except praw.exceptions.APIException as e:
            print("Rate limit exceeded")
            err_buffer += rf.bufferError("Rate limit exceeded. Sleeping for 1 minute.")
            time.sleep(60)
        except TypeError:
            print("TypeError found")
        if (id_buffer != ""):
            rf.logRespondedToID(RESPONDED_TO_FILE, id_buffer)
        id_buffer = ""
comments = reddit.subreddit("all").stream.comments()
#comments = reddit.subreddit("pepperbotsuite").comments() #use this if you want the bot to run in certain subreddits only
searchComments(comments)