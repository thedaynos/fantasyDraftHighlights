import re, requests,json
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
        print ("\n\nConnected to: "+chromeCastName+". Ready to Draft!")
    except StopIteration:
        print ("\n\n"+chromeCastName+" not found, vids will be displayed on this pc")
        chromeCast=False

if "sleeper" in site:
    import time
    site=="sleeper"
    from vDictSleeper import vDictSleeper as vDict
elif "clicky" in site:
    site=="clicky"
    from vDictClicky import vDictClicky as vDict

if chromeCast==False or site=="clicky":
    from selenium import webdriver
    prefs={"profile.default_content_setting_values.notifications":2}
    if site=="clicky":
        draftOptions=webdriver.ChromeOptions()
        draftOptions.add_experimental_option("prefs",prefs)
        draftOptions.add_argument('disable-infobars')
        if clickySiteVisible==False:
            draftOptions.add_argument("--headless")
            draftDriver=webdriver.Chrome(chrome_options=draftOptions)
        draftDriver.get('https://clickydraft.com/draftapp/board/'+str(boardNum))

sApi="https://api.sleeper.app/v1/draft/"+str(boardNum)+"/picks"
yt="https://youtube.com/tv#/watch?v="    
ytSearch="https://www.youtube.com/results?search_query="

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
while (True):
    if site=="clicky":
        html=draftDriver.page_source
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
        time.sleep(1)
        while (True):
            try:
                response = requests.get(sApi)
                yJson=json.loads(response.text)
                break
            except requests.exceptions.RequestException:
                yJson=""
                print ("call to: "+sApi+" failed, trying again in 5 seconds")
                time.sleep(5)
        for x in range(0,len(yJson)):
            pos=yJson[x]["metadata"]["position"]+yJson[x]["metadata"]["team"]
            fName=yJson[x]["metadata"]["first_name"]
            lName=yJson[x]["metadata"]["last_name"]
            thisPlayer=[pos,fName,lName]
            vStr=pos+fName+lName
            pTable=addPlayer(thisPlayer,pTable,choiceActive,vDict,vStr,fName,lName)
    choiceActive=True
    if len(pTable)>=(teams*rounds):
        break
if site=="clicky":
    draftDriver.quit()
if chromeCast==False:
    print("\n\nDraft completed! YouTube window will close in 5 minutes.\n\n")
    time.sleep(300)
    youTubeDriver.quit()
