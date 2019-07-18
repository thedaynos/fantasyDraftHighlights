from selenium import webdriver
import re
from vDict import *
from config import *

s=re.compile('[^a-zA-Z]')
def findTag(html,x):
    xhtml=html[html.find(x)+len(x):]
    end=xhtml.find('<')
    return s.sub('',xhtml[:end]),xhtml
prefs={"profile.default_content_setting_values.notifications":2}
cDraftOptions=webdriver.ChromeOptions()
cDraftOptions.add_experimental_option("prefs",prefs)
if not clickyDraftWebSiteVisible:
    cDraftOptions.add_argument("--headless")
clickyDriver=webdriver.Chrome(chrome_options=cDraftOptions)
clickyDriver.get(('https://clickydraft.com/draftapp/board/'+str(boardNum)))
youTubeOptions=webdriver.ChromeOptions()
youTubeOptions.add_argument("user-data-dir=youTube")
youTubeOptions.add_argument("--start-maximized")
youTubeOptions.add_experimental_option("prefs",prefs)
youTubeDriver=webdriver.Chrome(chrome_options=youTubeOptions)

pTable=[]
choiceActive=False
yt="https://youtube.com/tv#/watch?v="
while (True):
    html=clickyDriver.page_source
    html=html[html.find("<tbody>"):html.find("</tbody>")]
    for x in range (0,teams*rounds):
        html=html[html.find('class="pickContents"'):]
        pos,html=findTag(html,'class="playerPos">')
        team,html=findTag(html,'class="playerTeam">')
        fName,html=findTag(html,'class="playerFName">')
        lName,html=findTag(html,'class="playerLName">')
        thisPlayer=[pos,team,fName,lName]
        if thisPlayer not in pTable:
            try:
                vLink=vDict[pos+team+fName+lName]
            except KeyError:
                vLink=""
            if choiceActive and vLink!="":
                youTubeDriver.get(yt+vLink)
            pTable.append(thisPlayer)
    choiceActive=True
    if len(pTable)>=(teams*rounds):
        break
youTubeDriver.quit()
clickyDriver.quit()
