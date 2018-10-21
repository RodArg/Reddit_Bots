## Requirements:

Do a pip install of the following library:
pip install requests

* (info: http://docs.python-requests.org)

## What This Bot Does:

Hello, WebSafetyBot is a neat Reddit bot that can make sure the links you find while browsing
on Reddit are clean. 

On the darker, lesser known depths of Reddit, sometimes people will have hyperlinks on their comments that we don't really know how safe they are. Instead of having to check yourself whether that URL leads to a safe site or not, WebSafetyBot can do that for you.

The bot uses the Google Safe Browsing API v4 to check how safe websites are.

* (info: https://developers.google.com/safe-browsing/)

## How it Works:

After you find a comment with some links you're suspicious of, reply to that comment with the following text:

`!Facecheck`

The bot will then reply to your comment and let you know whether the URLS in the comment you replied to are safe or not. 
You'll also get some nice gifs to go along with them!

Let me know if you have any questions about the code or if the bot isn't working properly.
