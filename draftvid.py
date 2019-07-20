from selenium import webdriver
import re, requests
from config import *

if chromeCast:
    import pychromecast
    from pychromecast.controllers.youtube import YouTubeController
    chromecasts=pychromecast.get_chromecasts()
    try:
        cast = next(cc for cc in chromecasts if cc.device.friendly_name==chromeCastName)
        cast.wait()
        ytc=YouTubeController()
        cast.register_handler(ytc)
    except StopIteration:
        print ("cast not found, vids will be displayed on this pc")
        chromeCast=False

s=re.compile('[^a-zA-Z]')

def findTag(html,x):
    if html.find(x)!=-1:
        xhtml=html[html.find(x)+len(x):]
        end=xhtml.find('<')
    else:
        return -1,html
    return s.sub('',xhtml[:end]),xhtml

def addPlayer(thisPlayer,pTable,choiceActive,vDict,vStr,fName,lName):
    if thisPlayer not in pTable:
        try:
            vLink=vDict[vStr]
        except KeyError:
            vLink=""
        if choiceActive:
            if vLink!="":
                if chromeCast:
                    ytc.play_video(vLink)
                else:
                    youTubeDriver.get(yt+vLink)
            elif autoSearch:
                try:
                    url=ytSearch+fName+"+"+lName+"highlights"
                    response = requests.get(url)
                    yhtml=response.text
                except requests.exceptions.RequestException:
                    yhtml=""
                if yhtml!="":
                    yhtml=yhtml[yhtml.find('href="/watch?v=')+15:]
                    vLink=yhtml[:yhtml.find('"')]
                    if chromeCast:
                        ytc.play_video(vLink)
                    else:
                        youTubeDriver.get(yt+vLink)
        pTable.append(thisPlayer)
    return pTable

if "sleeper" in site:
    site=="sleeper"
elif "clicky" in site:
    site=="clicky"
yt="https://youtube.com/tv#/watch?v="    
ytSearch="https://www.youtube.com/results?search_query="
prefs={"profile.default_content_setting_values.notifications":2}
draftOptions=webdriver.ChromeOptions()
draftOptions.add_experimental_option("prefs",prefs)
draftOptions.add_argument('disable-infobars')
if site=="sleeper":
    draftDriver=webdriver.Chrome(chrome_options=draftOptions)
    from vDictSleeper import *
    vDict=vDictSleeper
    import time
    draftDriver.get('https://sleeper.app')
    time.sleep(time_to_login)
    if draftSiteVisible==False:
        draftDriver.minimize_window()
    draftDriver.get('https://sleeper.app/draft/nfl/'+str(boardNum))
elif site=="clicky":
    from vDictClicky import *
    vDict=vDictClicky
    if draftSiteVisible==False:
        draftOptions.add_argument("--headless")
        draftDriver=webdriver.Chrome(chrome_options=draftOptions)
    draftDriver.get('https://clickydraft.com/draftapp/board/'+str(boardNum))
if chromeCast==False:
    youTubeOptions=webdriver.ChromeOptions()
    youTubeOptions.add_argument("user-data-dir=youTube")
    youTubeOptions.add_argument("--start-maximized")
    youTubeOptions.add_argument("--kiosk")
    youTubeOptions.add_argument('disable-infobars')
    youTubeOptions.add_experimental_option("prefs",prefs)
    youTubeDriver=webdriver.Chrome(chrome_options=youTubeOptions)
pTable=[]
choiceActive=False
html=draftDriver.page_source
while (True):
    html=draftDriver.page_source
    if site=="clicky":
        html=html[html.find("<tbody>"):html.find("</tbody>")]
        for x in range (0,teams*rounds):
            html=html[html.find('class="pickContents"'):]
            pos,html=findTag(html,'class="playerPos">')
            team,html=findTag(html,'class="playerTeam">')
            fName,html=findTag(html,'class="playerFName">')
            lName,html=findTag(html,'class="playerLName">')
            thisPlayer=[pos,team,fName,lName]
            vStr=pos+team+fName+lName
            pTable=addPlayer(thisPlayer,pTable,choiceActive,vDict,vStr,fName,lName)
    elif site=="sleeper":
        for x in range(0,teams*rounds):
            pos,html=findTag(html,'class="position">')
            if pos==-1:
                break
            fName,html=findTag(html,'class="first-name">')
            lName,html=findTag(html,'class="last-name">')
            thisPlayer=[pos,fName,lName]
            vStr=pos+fName+lName
            pTable=addPlayer(thisPlayer,pTable,choiceActive,vDict,vStr,fName,lName)
    choiceActive=True
    if len(pTable)>=(teams*rounds):
        break
if chromeCast==False:
    youTubeDriver.quit()
draftDriver.quit()
