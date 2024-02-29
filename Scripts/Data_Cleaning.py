#!/usr/bin/env python
# coding: utf-8

# In[63]:


import pandas as pd
import os
from glob import glob
import re
import requests
import shutil



#scopusIndia = pd.read_csv('../Data/scopus_2021_physics.csv')


# In[65]:


#print (scopusIndia.columns)
#scopusIndiaSubset = scopusIndia[['Authors','Author(s) ID','Title','Year','Source title','Cited by','DOI',
#                               'Link','Document Type',
#                                'Source']]


# In[66]:


#scopusIndiaSubset.to_csv('../Data/Scopus_IndianPub_aft_2021_SUBSET_COL_physics.csv')


# In[ ]:





# # Getting URL Data

# In[115]:


import pandas as pd
from bs4 import BeautifulSoup # BeautifulSoup is in bs4 package 
import requests
# import browsercookie
from selenium import webdriver
from tqdm import tqdm_notebook as tqdm
import csv
import time
import re
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--headless")
chrome_options.add_argument('disable-blink-features=AutomationControlled')
chrome_options.add_argument('user-agent=fake-useragent')
chrome_options.add_argument('--user-data-dir=~/.config/google-chrome')
chrome_options.headless = True # also works
driver = webdriver.Chrome(options=chrome_options)


# In[280]:


file_ = pd.read_csv('../Data/Data/Researcher-Discovery-NLP.csv')


# In[260]:


file_sample =file_.head()


# In[46]:


# cj = browsercookie.chrome()
# head = {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'}
# r = requests.get("https://www.scopus.com/inward/record.uri?eid=2-s2.0-85063475493&doi=10.1007%2f978-3-030-11680-4_34&partnerID=40&md5=1bb96829daaa49a24a6be160d88beea0", cookies=cj,headers = head)
# soup = soup = BeautifulSoup(r.text, 'html.parser')#html.parser


# In[299]:


username ='priyankagupta@ms.du.ac.in'
password = 'Priya@1989'


# In[ ]:


#driver.get('https://id.elsevier.com/as/authorization.oauth2?platSite=SC%2Fscopus&ui_locales=en-US&scope=openid+profile+email+els_auth_info+els_analytics_info+urn%3Acom%3Aelsevier%3Aidp%3Apolicy%3Aproduct%3Aindv_identity&response_type=code&redirect_uri=https%3A%2F%2Fwww.scopus.com%2Fauthredirect.uri%3FtxGid%3D092a214d300ac62ef7553cb9e1f65f3f&state=userLogin%7CtxId%3DA7320C2C7F38D138ED975DBFAB4BFA25.i-037e98c7be7ddc14a%3A5&authType=SINGLE_SIGN_IN&prompt=login&client_id=SCOPUS')
#time.sleep(10)




#driver.find_element_by_css_selector('#bdd-elsSecondaryBtn').click()
#driver.find_element_by_id("bdd-email").send_keys(username)
#driver.find_element_by_css_selector("#bdd-els-searchBtn").click()
#driver.find_element_by_id("bdd-password").send_keys(password)
#driver.find_element_by_css_selector("#bdd-elsPrimaryBtn").click()


# In[128]:
print("logged in",file_.columns)

def get_name(html):
#     url = "https://www.scopus.com/authid/detail.uri?authorId=57205693172&amp;eid=2-s2.0-85061119789"
#     print url
#     driver.get(url) 
#     html = driver.page_source
    nameU = BeautifulSoup(html, "html.parser")
#     authInfo = nameU.find("div",{"class":"authInfoSection"})
    affil = nameU.find("div",{"class":"scopus-institution-name-link"})
    affiliation = affil.find("span")
#     country = affil.find(text=True,recursive=False)
#     print affil.text
    authN = nameU.find("h2",{"class":"author-general-details-title margin-size-4-t"})
    authName =''
    if authN:
        authName = authN.find(text=True,recursive =False)
    affiliat = ''
    if not authName:
        authName = ''
    if not affiliation:
        affiliat = ''
    else:
        affiliat = affiliation.text 
    print("Name",authName,affiliat)
    return(authName,affiliat)


# In[ ]:




abstract_ ='#profileleftinside > micro-ui > scopus-document-details-page > div > els-stack > article > div:nth-child(4) > section > div > div.margin-size-4-t.margin-size-16-b > els-typography > span'
author_keywords = '#profileleftinside > micro-ui > scopus-document-details-page > div > els-stack > article > div:nth-child(4) > section > div > div:nth-child(4)'
eng_controlled = '#indexed-keywords > section > div > div > els-stack > els-stack:nth-child(1) > dl > dd'
eng_uncontrolled = '#indexed-keywords > section > div > div > els-stack > els-stack:nth-child(2) > dl > dd'
eng_main_heading = '#indexed-keywords > section > div > div > els-stack > els-stack:nth-child(3) > dl > dd'
scival_tName ='#topics-of-prominence > section > div > div > div > dl > div.row.margin-size-12-b > dd > button > span'
scival_ = '#topics-of-prominence > section > div > div > div > dl > div:nth-child(2) > dd > span'
for index in range (0,file_.shape[0]):
    link = file_.iloc[index]['Link']
    authors = str(file_.iloc[index]['Authors'])
    title = str(file_.iloc[index]['Title'])
    source_title = str(file_.iloc[index]['Source title'])
    year = str(file_.iloc[index]['Year'])
    aff = str(file_.iloc[index]['Author(s) ID'])
    cited_count = str(file_.iloc[index]['Cited by'])
#     print(type(year),type(aff),type(cited_count),type(link))
    
    print( index,link)
    driver.get(link)
#     wait = WebDriverWait(driver, 10)
    time.sleep(6)
    try:
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        dict_ = {'Abstract':'','Author_Keywords':'','Eng_controlled':'','Eng_Uncontrolled':'',
                'Eng_main_heading':'','Scival_topic':'','Scival_Score':-1}
        abstract = soup.select(abstract_)
        author_key =soup.select(author_keywords)
        eng_controlled_key = soup.select(eng_controlled)
        eng_uncontrolled_key = soup.select(eng_uncontrolled)
        eng_heading_key = soup.select(eng_main_heading)
        scival_tname = soup.select(scival_tName)
        scival_score = soup.select(scival_)
        
        if len(abstract)>0:
            dict_['Abstract'] = abstract[0].text
        if len(author_key)>0:
            dict_['Author_Keywords'] = author_key[0].text
        if len(eng_controlled_key)>0:
            dict_['Eng_controlled'] = eng_controlled_key[0].text
        if len(eng_heading_key)>0:
            dict_['Eng_main_heading'] = eng_heading_key[0].text
        if len(eng_uncontrolled_key)>0:
            dict_['Eng_Uncontrolled'] = eng_uncontrolled_key[0].text
        if len(scival_tname)>0:
            dict_['Scival_topic'] = scival_tname[0].text
        if len(scival_score)>0:
            dict_['Scival_Score'] = scival_score[0].text
        print('found')
#         Below code is Working . Uncomment if you want to extract author emails and affilations
#         f = soup.select('#profileleftinside > micro-ui > scopus-document-details-page > div > els-stack > article > div:nth-child(1) > section > div:nth-child(3) > div > ul > li')
#         print(len(f))
#         for ind, li in enumerate(f):
#             all_list =li.find_all('els-button')
#             dict_={'AuthorName':'','Affiliation':'','Email':''}
#             for m in all_list:
#                 if m['variant']=='link':
#                     dict_['AuthorName'] = m.text
#                 if 'href' in list(m.attrs.keys()):
#                     dict_['Email'] = m['href'].split('mailto:')[-1]

#                     driver.find_element_by_css_selector('#profileleftinside > micro-ui > scopus-document-details-page > div > els-stack > article > div:nth-child(1) > section > div:nth-child(3) > div > ul > li:nth-child('+str(ind+1)+') > els-button').click()
#                     page_source = driver.page_source
#                     soup2 = BeautifulSoup(page_source,'html.parser')
#                     affilation =soup2.select('#author-preview-flyout > div > div > div > div > div.flyout__dialog--content-slot > div > els-focus-trap > section > els-stack > els-stack.stack.stack--l.stack--mode-normal.stack--vertical.stack--start.hydrated > els-stack.stack.stack--s.stack--mode-normal.stack--vertical.stack--start.hydrated > els-stack > span > els-button')
#     #                 print("affiliation",affilation,type(affilation))
#                     driver.find_element_by_css_selector('#author-preview-flyout > div > div > div > div > div.flyout__dialog--content-slot > div > els-focus-trap > section > header > button > span.button__icon > els-icon > svg').click()
#                     if len(affilation)==0:
#                         dict_['Affiliation']=''
#                     else:
#                         dict_['Affiliation']=affilation[0].text
#                 dfP  = pd.DataFrame([dict_], columns=dict_.keys())
#                 with open('../Data/AuthorDetails_Gr2021_physics.csv',mode='a') as dump:
#                     csv_data = re.sub(",","_",dict_['AuthorName'])+","+re.sub(","," ",dict_['Affiliation'])+","+re.sub(","," ",dict_['Email'])+","
#                     print(csv_data)
#                     dump_data = csv.writer(dump, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#                     dump_data.writerow(csv_data.split(","))
        with open('../Data/Paper_Details/PaperDetails_Gr2021_NLP1.csv',mode='a') as dump:
            csv_data = re.sub(",","_",authors)+","+re.sub(","," ",title)+","+re.sub(","," ",source_title)+","+re.sub(","," ",year)+","+re.sub(","," ",link)+","+re.sub(","," ",cited_count)+","+re.sub(",","_",dict_['Abstract'])+","+re.sub(","," ",dict_['Author_Keywords'])+","+re.sub(","," ",dict_['Eng_controlled'])+","+re.sub(","," ",dict_['Eng_Uncontrolled'])+","+re.sub(","," ",dict_['Eng_main_heading'])+","+re.sub(","," ",dict_['Scival_topic'])+","+re.sub(","," ",str(dict_['Scival_Score']))
            print(csv_data)
            dump_data = csv.writer(dump, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            dump_data.writerow(csv_data.split(","))
    except:
        print(index,"error")




