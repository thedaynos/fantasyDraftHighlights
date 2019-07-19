# Fantasy Draft AutoHighlight Viewer

Real simple python program that reads clickydraft or sleeperbot draft boards to enhance your draft party by automatically playing a highlight video of the player who just got selected.

## Getting Started

This only will work with clickydraft and sleeperbot (For now) and youtube (also for now), and chrome web browser (maybe add onto that later, who knows). Just download the files to a directory anywhere you like.

This hasn't been super thoroughly tested and there could be bugs, but I've tested it quite a bit while creating it and I'm pretty sure I got everything.  If you find a bug please contact me. 

### Prerequisites

OS: I ran this on my raspberry pi and windows 7 and 10 systems no problem. 
Software: Chrome browser
Python Version 3
Package: requests. You will need to install requests
```
pip install requests
```
Package: selenium. You will also need to install selenium.  
```
pip install selenium
```

Once you've done that, download the "webdriver" for the version of chrome that you're running. Simple google search should help you find this and the instructions for what to do with the webdriver when you get it. 
```
https://sites.google.com/a/chromium.org/chromedriver/downloads
```

### Installing

Download all the files and put them all in the same folder.

After you've created your clickydraft or sleeperbot draft board, you will need to edit the config.py file.
Open it up with any text editor.  
That file is small and only contains a few lines.  Here's how it looks when you download it.

```

site="sleeper"
teams=12
rounds=16
draftSiteVisible=False
boardNum=12345
time_to_login=30
autoSearch=True

```
Super simple stuff here. Change your teams and rounds to the number of teams and rounds in your draft.  

If you're using clickydraft then enter site="clicky"
If you're using sleeperbot then enter site="sleeper"
If you have anything else in there, the app won't run correctly.  

BoardNum is the number on the end of your clickydraft or sleeperbot URL.

```
https://clickydraft.com/draftapp/board/12345
https://sleeper.app/draft/nfl/12345
```

If this is what your URL looks like then the boardNum is 12345

Sleeper boardNum's are pretty long, like 18 digits.  Best to copy/paste it.

The variable "draftSiteVisible" can be set to True or False (capitalization is important). Default is False.

If you set it to True then the draft site will pop up on your screen.  If you set it to False then it won't.  
I prefer False because the point of this app is to display highlight videos, so this screen shouldn't generally be displaying a draft board. 
You can change it to True if you want to. Maybe if you're running multiple monitors or want to troubleshoot or whatever.  All good, your choice. Just make sure it's True or False.

time_to_login is the amount of seconds it takes you to login to your sleeperbot site.  In order to use this with sleeperbot drafts, you need to login with an account that's connected to that draft.  If you're a quick typer then 15 seconds should be enough.  If not, try 30-45 seconds.  Login isn't needed for clickydraft drafts, so if you're only using this for clicky then ignore this setting.

The last option is "autoSearch" which can be either True or False.

If it's set to True, the program will go out and search youtube for the first highlight reel it can find for that player name.  

This is going to work fine for most players, however some players have common names so the youtube search might return a vid for a different player in a different sport.

You can change this behavior by placing a specific youtube video link of your choice in the vDict file for either sleeperbot or clickydraft. 

```
vDictClicky.py
vDictSleeper.py
```

Both of these files are in your folder already.  The code will look in the correct file and grab whatever link you have placed in that player's entry in the dictionary.  

If there is no link, then it will auto search on youtube.

You can stop the auto search functionality altogether with autoSearch=False .  If you do this, then the code will ONLY play videos for the links that you provide in the dictionary. 

Here's how the first few lines of the dictionary files look after you download...
(using the vDictSleeper.py sleeperbot file since most of the users are on sleeper and not clicky)

```
vDictSleeper ={
    "RBNYGSaquonBarkley":"",
    "RBARIDavidJohnson":"",
    "RBNOAlvinKamara":"",
    "RBDALEzekielElliott":"8CJvUpV2jp0",
    "WRHOUDeAndreHopkins":"",
    "RBCARChristianMcCaffrey":"",

```

As you can see, there's one line for each player, and I've included an example of what the link should look like for Ezekiel Elliot.   Do NOT change the first part of each line before the colon. The app uses that part to lookup each player as it's picked. If you change that part, the code will not be able to find anything for that player. It's very picky.

The capitalization here also matters.  I've taken out all non-alphabetic characters out of the players' names like apostrophes, spaces, dashes, etc.

Going back to the Zeke example:  

```
    "RBDALEzekielElliott":"8CJvUpV2jp0",
```

That will tell the code that when zeke is picked, it will pull up the following link:
```
https://youtube.com/tv#/watch?v=8CJvUpV2jp0
```

If you don't want a specific vid for a player, and you WANT the auto search, then you need to delete everything between the quotes. So a player without a specific vid link will have two double quotes at the end, followed by a comma. 
Like this:

```
    "RBDALEzekielElliott":"",
```
Any change in that will probably cause problems.

If you don't want ANY vid for that player, no matter what, then either delete his entry or put a hashtag at the beginning of the line. 
Like this:
```
#    "RBDALEzekielElliott":"",
```


I've included over 600 possible players that you're allowed to draft in the apps. So you are set even if you have up to 32 team, 18 round draft :)

And I've already assigned specific links for all defensive team highlights.  Honestly some teams didn't have a lot of defensive highlights from last year so I did the best I could on minimal effort.

## To Run

Before running, make sure you've closed out of all of your open chrome windows. 

At your command line, in your installed directory, type: 

```
python draftvid.py
```

If you are using sleeperbot, you will be presented with sleeperbot's home page and at this point you have to click "login" to log in to your account.  

You'll have whatever amount of time you listed in the config.py file (default is 30 seconds).  If you finish it early, just wait the remaining amount of time. The screen will minimize and then the new browser for your youtube vids will pop up.

If you are using clicky, then you don't need to log into your account. The main chrome browser for youtube will load right away.

This app is best used when you run it on a computer and then output the video of that computer to a big screen TV.  Then enter the picks on a different device, like your phone or another laptop.  Makes the experience a lot cooler.

One thing I should mention is that the first time you run this, youtube will play an ad.  For whatever reason it always does this on fresh installs and the first time you run it every day. But then afterwards, the ad doesn't pop up anymore. I guess it depends on youtube's mood at the time but sometimes you're gonna get an ad here and there.  If you can figure out how to block youtube ads, please IM me lol.  


## Author

I am thedaynos and I have a patreon if you feel like donating to my "i don't code for free (actually i guess i do) foundation"
https://www.patreon.com/thedaynos

msg me on reddit if you have questions or find a bug.  /u/thedaynos
