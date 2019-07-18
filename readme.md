# Fantasy Draft Highlight Player

Real simple python program that reads clickydraft drafts to enhance your draft party by automatically playing a highlight video of the player selected.

## Getting Started

This only will work with clickydraft (For now) and youtube (also for now), and chrome web browser (maybe add onto that later, who knows). Just download the files to a directory anywhere you like.

This hasn't been super thoroughly tested and there could be bugs, but I've tested it quite a bit while creating it and I'm pretty sure I got everything.  If you find a bug please contact me. 

### Prerequisites

OS: I ran this on my raspberry pi and windows 7 and 10 systems no problem. 
Software: Chrome browser
Python Version 3
Packages: selenium. You will need to install selenium
```
pip install selenium
```

Once you've done that, download the "webdriver" for the version of chrome that you're running. Simple google search should help you find this and the instructions for what to do with the webdriver when you get it. 
```
https://sites.google.com/a/chromium.org/chromedriver/downloads
```

### Installing

Download the 3 files and put them all in the same folder.

After you've created your clickydraft board, you will need to edit the config.py file.
Open it up with any text editor.  
In that file is a few lines.  Here's how it looks when you download it.

```

teams=12
rounds=16
boardNum=12345
clickyDraftWebSiteVisible=False

```
Super simple stuff here. Change your teams and rounds to the number of teams and rounds in your draft.  BoardNum is the number on the end of your clickydraft URL.

```
https://clickydraft.com/draftapp/board/12345
```

If this is your URL then the boardNum is 12345

The variable "clickyDraftWebSiteVisible" can be set to True or False (capitalization is important).
If you set it to True then the draft site will pop up on your screen.  If you set it to False then it won't.  
I prefer False because this screen should generally only be used for displaying the youtube highlight videos.
You can change it to True if you want to. Maybe if you're running multiple monitors or waht to troubleshoot?  All good, your choice.

Don't put anything else in here.

Then there's the vDict.py file.

This file is where you're going to paste your youtube video links for each player.  (vDict stands for Video Dictionary)

Here's how the first few lines of this file look after you download it...

```
vDict = {
    "RBNYGSaquonBarkley":"",
    "RBDALEzekielElliott":"8CJvUpV2jp0",
    "RBCARChristianMcCaffrey":"",
    "RBNOAlvinKamara":"",
    "RBARIDavidJohnson":"",
    "WRHOUDeAndreHopkins":"",
```

As you can see, there's one line for each player.   Do NOT change the first part of each line. This first part is how the program is going to lookup each player as it's picked.
I realize people who are using this probably are fantasy football savvy already but in case you're not, the format is:
Position, Team Abbreviation, First Name, Last name
The capitalization here also matters so don't mess with anything.  I've taken out all non-alphabetic characters out of the players' names like apostrophes, spaces, dashes, etc.

Also I've already started you out here with a youtube link for ezekiel elliot's highlights.  

```
    "RBDALEzekielElliott":"8CJvUpV2jp0",
```

That will tell the code that when zeke is picked, it will pull up the following link:
```
https://youtube.com/tv#/watch?v=8CJvUpV2jp0
```

It's your job to go through the rest of the players to find their highlight reels on youtube (whichever ones you prefer) and insert them in between the quotations.  

Do not forget that there needs to be a comma after each player except for the very last one on the list.  

I've included over 600 possible players that you're allowed to draft in clickydraft. So you are set even if you have up to 32 team, 18 round draft :)


## To Run

At your command line, in your installed directory, type: 

```
python draftvid.py
```

My personal preference is to let this run on a computer and then output the video of that computer to a big screen TV.  Then enter the picks on a different device, like your phone or another laptop.  Makes the experience a lot cooler.

One thing I should mention is that the first time you run this, youtube will play an ad.  For whatever reason it always does this on fresh installs. But then afterwards, the ad doesn't pop up anymore. I guess it depends on youtube's mood at the time but sometimes you're gonna get an ad here and there.  If you can figure out how to block youtube ads, please IM me lol.  


## Author

I am thedaynos and I have a patreon if you feel like donating to my "i don't code for free (actually i guess i do) foundation"
https://www.patreon.com/thedaynos

msg me on reddit if you have questions or find a bug.  /u/thedaynos
