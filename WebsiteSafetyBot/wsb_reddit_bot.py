from WebsiteSafetyBot import keys
from WebsiteSafetyBot.gglsb_lookup import checkWebsite
import praw

#Message that will trigger the bot
trigger = "!facecheck"

#If you'll post a link with your message, url is true
adding_gif = False
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
    comments = submission.comments

    #Go through the comments of each submission
    for comment in comments:
        text = str(comment.body)
            #print(text) #in case you want to print out the comments
        if(trigger in text.lower()):
            ##This has to be changed to find the url within the comment text itself
            text = text.split("!Facecheck")
            #print(text)
            text = text[1]
            response = checkWebsite(text)
            status_code = response[0]
            threat = response[1]

            message = threatResponse[threat]

            if(threat == "ERROR"):
                message = "ERROR: " + status_code + message
            else:
                #Formats reply to make the url a hyperlink
                message = "[" + message + "](" + gifs[threat] + ")"
            comment.reply(message)