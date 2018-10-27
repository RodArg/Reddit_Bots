import keys
import wsb_ggsb_lookup
import wsb_reddit_functions as rf
import praw
import re
import time

LOG_FILE = "wsb_logs.txt"
REPLIED_TO_FILE = "wsb_ids.txt"
SUBREDDITS_FILE = "wsb_subreddits.txt"

#Regex to find all urls within parent text body #credit: GooDeeJaY answering at stackoverflow
REGEX_URL = '(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+'
SUB_AMT = 6 #Number of submissions to go through

trigger = "!facecheck"

#Message components
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
submission_ids = rf.getSubmissions(reddit, subreddits, SUB_AMT) #will be a list

def botAction(id):
    if(id == False):
        return
    message = ""
    comment = reddit.comment(id=id)
    print("comment:", comment.body)
    parent = reddit.comment(id=comment.parent())
    parent_txt = str(parent.body)
    urls = re.findall(REGEX_URL, parent_txt)
    for url in urls:
        response = wsb_ggsb_lookup.checkWebsite(url)
        status_code = response[0]
        threat = response[1]
        body = threatResponse[threat]
        if (threat == "ERROR"):
            return (status_code + body, url)
        else:
            # Formats reply to make the url a hyperlink
            url = rf.unlinkURL(url)
            #print("Proper url:", url)
            body = url + "|" + rf.buildHyperlink(body, gifs[threat])
        message += body + "\n"
    if (message != ""):
        message = head + message + signature
        print("Printing Message:",message)
        comment.reply(message)
        time.sleep(2)
    return False

def runBot():
    running = True
    id_buffer = ""
    err_buffer = ""
    while(running):
        try:
            print("1")
            replied_to_ids = rf.getRepliedToIDs(REPLIED_TO_FILE)
            print("2")
            comments = rf.findCommentID(reddit, submission_ids, trigger)
            print("3")
            for comment in comments:
                parent = comment.parent()
                if(rf.haveRepliedTo(parent, replied_to_ids)):
                    print("Already replied to /u/", comment.author.name)
                    comment = False
                if(comment != False): #if we found our trigger
                    #print("Found trigger")
                    id_buffer += rf.bufferResponseID(str(parent))
                failed = botAction(comment)
                if(failed):
                    print("Failed")
                    errorString = "|URL: " + failed[0] + "|Body: " + "ERROR:" + failed[1]
                    err_buffer += rf.bufferError(errorString)
            #running = False
        except KeyboardInterrupt:
            running = False
        # log all buffers
        rf.logResponseID(REPLIED_TO_FILE, id_buffer)
        rf.logError(LOG_FILE, err_buffer)
runBot()