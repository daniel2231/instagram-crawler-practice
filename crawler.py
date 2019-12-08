from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import datetime


driver = webdriver.Chrome()

driver.get('https://www.instagram.com/p/Bt-gkAJAZF6/?utm_source=ig_web_copy_link')
soup = BeautifulSoup(driver.page_source,"lxml")
desc = " "

for item in soup.findAll('a'):
    desc= desc + " " + str(item.string)

taglist = desc.split()
taglist = [x for x in taglist if x.startswith('#')]
index = 0
while index < len(taglist):
    taglist[index] = taglist[index].strip('#')
    index += 1

#taglist = []

print(taglist)

tag_df  = pd.DataFrame(columns = ['Hashtag', 'Number of Posts', 'Posting Freq (mins)'])

for tag in taglist:
    
    driver.get('https://www.instagram.com/explore/tags/'+str(tag))
    soup = BeautifulSoup(driver.page_source,"lxml")
    
    tagname = tag
    nposts = soup.find('span', {'class': 'g47SY'}).text
        
    myli = []
    for a in soup.find_all('a', href=True):
        myli.append(a['href'])

    newmyli = [x for x in myli if x.startswith('/p/')]
    del newmyli[:9]
    del newmyli[9:]
    del newmyli[1:8]

    timediff = []

    for j in range(len(newmyli)):
        driver.get('https://www.instagram.com'+str(newmyli[j]))
        soup = BeautifulSoup(driver.page_source,"lxml")

        for i in soup.findAll('time'):
            if i.has_attr('datetime'):
                timediff.append(i['datetime'])
                #print(i['datetime'])


    datetimeFormat = '%Y-%m-%dT%H:%M:%S.%fZ'
    diff = datetime.datetime.strptime(timediff[0], datetimeFormat)\
        - datetime.datetime.strptime(timediff[1], datetimeFormat)
    pfreq= int(diff.total_seconds()/(9*60))
    
    tag_df.loc[len(tag_df)] = [tagname, nposts, pfreq]
        
driver.quit()

# Check the final dataframe
print(tag_df)

# CSV output for hashtag analysis
tag_df.to_csv('hashtag_list.csv')
