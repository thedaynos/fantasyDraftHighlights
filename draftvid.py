import re
import requests
import json
from config import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pychromecast.controllers.youtube import YouTubeController
import time

# Set up chromecast
if chromeCast:
    import pychromecast
    chromecasts = pychromecast.get_chromecasts()
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[chromeCastName])
    try:
        cast = chromecasts[0]
        cast.wait()
        ytc = YouTubeController()
        cast.register_handler(ytc)
        print("\n\nConnected to: " + chromeCastName + "!")
    except:
        print("\n\n" + chromeCastName + " not found, videos will be displayed on this screen")
        chromeCast = False

# Set up system variables for specific drafting sites
if "sleeper" in site.lower():
    site = "sleeper"
    sApi = "https://api.sleeper.app/v1/draft/" + str(boardNum) + "/picks"
    from vDictSleeper import vDictSleeper as vDict
elif "clicky" in site.lower():
    site = "clicky"
    from vDictClicky import vDictClicky as vDict
elif "basmith7" in site.lower():
    site = "basmith7"
    from vDictbasmith7 import vDictbasmith7 as vDict
elif "espn" in site.lower():
    site = "espn"
    from vDictEspn import vDictEspn as vDict
    mainUrl = "https://www.espn.com/fantasy/football/"
    boardUrl = "fantasy.espn.com/football/draft?leagueId="
elif "yahoo" in site.lower():
    site = "yahoo"
    from vDictYahoo import vDictYahoo as vDict
    mainUrl = "https://sports.yahoo.com/fantasy/"
    boardUrl = "football.fantasysports.yahoo.com/draftclient"
else:
    print("\n\n\nConfig Error\n\n")
    print('In the config file, the line site= must have a choice of: "espn", "yahoo", "sleeper", "clicky", or "basmith7".')
    import sys
    exit()

    # Initialize selenium drivers and open draft boards
if not chromeCast or site == "clicky" or site == "espn" or site == "yahoo":
    # These lines are needed for all cases that use selenium
    from selenium import webdriver
    prefs = {"profile.default_content_setting_values.notifications": 2}
    # This section is for draftboard selenium use cases (non-youtube)
    if site == "clicky" or site == "espn" or site == "yahoo":
        draftOptions = webdriver.ChromeOptions()
        draftOptions.add_experimental_option("prefs", prefs)
        draftOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
        draftOptions.add_argument('disable-infobars')
        draftOptions.add_extension('C:/extension_5_6_0_0.crx')
        # Cannot be headless for ESPN or Yahoo because you need to log in.
        if not draftBoardVisible and site != "espn" and site != "yahoo":
            draftOptions.add_argument("--headless")
        draftDriver = webdriver.Chrome(options=draftOptions)
        if site == "clicky":
            draftDriver.get('https://clickydraft.com/draftapp/board/' + str(boardNum))
        elif site == "espn" or site == "yahoo":
            draftDriver.get(mainUrl)
            url = ""
            print("Waiting for the user to open the " + site + " draft board")
            # Toggles through open tabs every 5 seconds to find your draft board.
            while True:
                for handle in draftDriver.window_handles:
                    draftDriver.switch_to.window(handle)
                    if boardUrl in draftDriver.current_url:
                        url = draftDriver.current_url
                        print("We found your board! Ready to Draft!!!")
                    elif site not in draftDriver.current_url:
                        draftDriver.close()
                if url != "":
                    break
                else:
                    time.sleep(5)
            # After the board is found, selenium loads it to give it focus
            draftDriver.get(url)
            # For Yahoo, it will click on "draft results" or else selenium can't see the picks
            if site == "yahoo":
                from selenium.common.exceptions import NoSuchElementException as NSE
                while True:
                    try:
                        resultsElement = draftDriver.find_element(By.XPATH, "//*[contains(text(), 'Draft Results')]")
                        resultsElement.click()
                        break
                    except NSE:
                        time.sleep(1)
            draftDriver.minimize_window()

# Setting up YouTube display for Selenium
if not chromeCast:
    options = {}
    youTubeOptions = webdriver.ChromeOptions()
    #youTubeOptions.add_argument("user-data-dir=youTube")
    youTubeOptions.add_argument("--start-maximized")
    youTubeOptions.add_argument("--kiosk")
    youTubeOptions.add_argument("--incognito")
    youTubeOptions.add_argument('disable-infobars')
    youTubeOptions.add_extension('C:/extension_5_6_0_0.crx')
    youTubeOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
    youTubeOptions.add_experimental_option("prefs", prefs)
    youTubeDriver = webdriver.Chrome(options=youTubeOptions)
    youTubeDriver.get("https://www.youtube.com")

#setting up youtube links
yt = "https://www.youtube.com/watch?v="
yt2 = "&feature=emb_rel_err"
ytSearch = "https://www.youtube.com/results?search_query="
# videoEmbeddable:"true"

# Functions to find tags if screen scraping is needed
import re

def findClickyTag(html, x):
    if html.find(x) != -1:
        xhtml = html[html.find(x) + len(x):]
        end = xhtml.find('<')
    else:
        return -1, html
    return re.sub('[^a-zA-Z]', '', xhtml[:end]), xhtml

def findbasmith7Tag(html):
    if html.find('1050371') < 0:
        return False, "", "", "", ""
    else:
        html = html[html.find('1050371') + 21:]
        fullName = html[:html.find('\\n')]
        posString = html[html.find('\\n') + 2:]
        dashLoc = posString.find(' - ')
        pos = posString[:dashLoc]
        team = posString[dashLoc + 3:dashLoc + 6]
        return True, re.sub('[^a-zA-Z]', '', fullName), pos, team, html

def findEspnTag(html):
    nText = '<span class="playerinfo__playername">'
    tText = '<span class="playerinfo__playerteam">'
    pText = '<span class="playerinfo__playerpos ttu">'
    aPos = html.find(nText)
    if aPos < 0:
        return html, "", "", ""
    html = html[html.find(nText) + len(nText):]
    fullName = html[:html.find('<')]
    html = html[html.find(tText) + len(tText):]
    team = html[:html.find('<')]
    html = html[html.find(pText) + len(pText):]
    pos = html[:html.find('<')]
    return html, fullName, team, pos

def findYahooTag(html):
    idText = '<td class="Ta-c">'
    fnText = ' class="ys-player">'
    teamText = '<abbr title="'
    posText = '<abbr class="Mstart-4" title="'
    aPos = html.find(idText)
    if aPos < 0:
        return html, "", "", ""
    html = html[html.find(fnText) + len(fnText):]
    thisPlayer = html[:html.find('</tr>')]
    fullName = thisPlayer[:thisPlayer.find('<')]
    if thisPlayer.find(teamText) == -1:
        pos = "DEF"
        return html, fullName, "", pos
    thisPlayer = thisPlayer[thisPlayer.find(teamText) + 1:]
    team = thisPlayer[thisPlayer.find('>') + 1:thisPlayer.find('<')]
    thisPlayer = thisPlayer[thisPlayer.find(posText) + 1:]
    pos = thisPlayer[thisPlayer.find('>') + 1:thisPlayer.find('<')]
    return html, fullName, team, pos

def findYahooD(html):  # need a separate function for defenses on yahoo
    idText = 'Fw-b ys-player Mstart-4'
    teamText = '<span class="Mstart-4"><abbr title="'
    posText = '<abbr title="">'
    if html.find(idText) == -1:
        return "", "", "", ""
    html = html[html.find(idText):]
    html = html[html.find('>') + 1:]
    fullName = html[:html.find('<')]
    html = html[html.find(teamText) + len(teamText):]
    html = html[html.find('>') + 1:]
    team = html[:html.find('<')]
    html = html[html.find(posText) + len(posText):]
    pos = html[:html.find('<')]
    return html, fullName, team, pos

    # This function plays the video found from YouTube
def playVid(vLink):
    if chromeCast:
        ytc.play_video(vLink)
    else:
        youTubeDriver.get(yt+vLink+yt2)
        try:
            playaE = youTubeDriver.find_element(By.ID, 'movie_player')
        except:
            nada = 0
        try:
            playaE.send_keys('f')
        except:
            nada = 0
    return

# Searches YouTube for link
def findVLink(fName, lName):
    try:
        url = ytSearch + fName + "+" + lName + "+highlights"
        response = requests.get(url)
        yhtml = response.text
        yhtml = yhtml[yhtml.find('href="/watch?v=')+15:]
        vLink = yhtml[:yhtml.find('"')]
        if "><" in vLink:
            yhtml = response.text
            yhtml = yhtml[yhtml.find('"videoId":"')+11:]
            vLink = yhtml[:yhtml.find('"')]
    except requests.exceptions.RequestException:
        vLink = ""
    return vLink

    # This function plays the video found from YouTube
def playVid(vLink):
    if chromeCast:
        ytc.play_video(vLink)
    else:
        youTubeDriver.get(yt + vLink + yt2)
        try:
            playaE = youTubeDriver.find_element(By.ID, 'movie_player')
        except:
            nada = 0
        try:
            playaE.send_keys('f')
        except:
            nada = 0
    return

# This function runs when a player is found on the draft board
def addPlayer(thisPlayer, pTable, choiceActive, vDict, vStr, fName, lName):
    if thisPlayer not in pTable:
        try:
            vLink = vDict[vStr]
        except KeyError:
            vLink = ""
        if choiceActive:
            if vLink != "":
                playVid(vLink)
            elif autoSearch:
                vLink = findVLink(fName, lName)
                if vLink != "":
                    playVid(vLink)
        pTable.append(thisPlayer)
    return pTable

def skipAds():
    if chromeCast == False:
        try:
            time.sleep(6)
            skipE = youTubeDriver.find_element(By.CLASS_NAME, "ytp-ad-skip-button-container")
            skipE.click()
            time.sleep(1)
        except:
            nada = 0
    return

#create player table
pTable = []

# choiceActive set to false at the beginning so the first player loop doesn't play
# videos for the players already entered.
choiceActive = False

while True:
    skipAds()
    if site == "clicky":
        html = draftDriver.page_source
        html = html[html.find("<tbody>"):html.find("</tbody>")]
        for x in range(0, teams * rounds):
            html = html[html.find('class="pickContents"'):]
            pos, html = findClickyTag(html, 'class="playerPos">')
            team, html = findClickyTag(html, 'class="playerTeam">')
            fName, html = findClickyTag(html, 'class="playerFName">')
            lName, html = findClickyTag(html, 'class="playerLName">')
            thisPlayer = [pos, team, fName, lName]
            vStr = pos + team + fName + lName
            pTable = addPlayer(thisPlayer, pTable, choiceActive, vDict, vStr, fName, lName)
    elif site == "sleeper":
        time.sleep(1)  # 1 second wait in between API calls
        while True:
            try:
                response = requests.get(sApi)
                yJson = json.loads(response.text)
                break
            except requests.exceptions.RequestException:
                yJson = ""
                print("Call to: " + sApi + " failed, trying again in 5 seconds")
                time.sleep(5)
        for x in range(0, len(yJson)):
            pos = yJson[x]["metadata"]["position"] + yJson[x]["metadata"]["team"]
            fName = yJson[x]["metadata"]["first_name"]
            lName = yJson[x]["metadata"]["last_name"]
            thisPlayer = [pos, fName, lName]
            vStr = pos + fName + lName
            pTable = addPlayer(thisPlayer, pTable, choiceActive, vDict, vStr, fName, lName)
    elif site == "basmith7":
        time.sleep(5)  # 5 second wait in between page requests
        while True:
            try:
                response = requests.get(basmith7URL)
                html = response.text
                break
            except requests.exceptions.RequestException:
                html = ""
                print("Call to: " + basmith7URL + " failed, trying again in 5 seconds")
                time.sleep(5)
        html = html[html.find("var bootstrapData = ") + 20:]
        html = html[:html.find(";")]
        while True:
            foundName, fullName, pos, team, html = findbasmith7Tag(html)
            if foundName:
                vStr = s.sub('', str(pos) + str(team) + str(fullName))
                thisPlayer = [pos, team, fullName]
                pTable = addPlayer(thisPlayer, pTable, choiceActive, vDict, vStr, "", fullName)
            else:
                break
    elif site == "espn":
        html = draftDriver.page_source
        while True:
            html, fullName, team, pos = findEspnTag(html)
            if fullName == "":
                break
            vStr = s.sub('', str(pos) + str(team) + str(fullName))
            thisPlayer = [pos, team, fullName]
            pTable = addPlayer(thisPlayer, pTable, choiceActive, vDict, vStr, "", fullName)
    elif site == "yahoo":
        html = draftDriver.page_source
        dhtml = html
        while True:
            html, fullName, team, pos = findYahooTag(html)
            if fullName == "":
                break
            if pos != "DEF":
                vStr = s.sub('', str(pos) + str(team) + str(fullName))
                thisPlayer = [pos, team, fullName]
                pTable = addPlayer(thisPlayer, pTable, choiceActive, vDict, vStr, "", fullName)
        while True:
            dhtml, fullName, team, pos = findYahooD(dhtml)
            if fullName == "":
                break
            if pos == "DEF":
                vStr = s.sub('', str(pos) + str(team) + str(fullName))
                thisPlayer = [pos, team, fullName]
                pTable = addPlayer(thisPlayer, pTable, choiceActive, vDict, vStr, "", fullName)
    choiceActive = True
    if len(pTable) >= (teams * rounds):
        break

if site == "clicky" or site == "espn" or site == "yahoo":
    draftDriver.quit()
if chromeCast == False:
    print("\n\nDraft completed! YouTube window will close in 5 minutes.\n\n")
    time.sleep(300)
    youTubeDriver.quit()
