import base64
import json
import requests
import os
import time
from dotenv import load_dotenv
load_dotenv()
Headers=(os.getenv('User'),os.getenv('token'))

def Analysis(url):
  res=url.split('github.com')[-1]
  URL = "https://api.github.com/repos"+res+"/commits"
  r = requests.get(url = URL,auth=Headers)
  data = r.json()
  dates={}
  timeline=[]
  for i in data:
    key=i["commit"]["author"]["date"].split('T')[0]
    if key not in dates:
      dates[key]=1
      timeline.append(key)
    else:  
      dates[key]+=1
  a=[int(i) for i in timeline[-1].split('-')]
  b=[int(i) for i in timeline[0].split('-')]
  span=(b[0]-a[0])*365+(b[1]-a[1])*30+(b[2]-a[2])+1
  return {'start':timeline[-1],'end':timeline[0],'stats':dates,'span': span}

def read(url):
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()
    file_content = data['content']
    file_content_encoding = data.get('encoding')
    if file_content_encoding == 'base64':
        file_content = base64.b64decode(file_content).decode()
    else:
        file_content=''
    return file_content

def assets(URL):
  r = requests.get(url = URL,auth=Headers)
  time.sleep(0.5)
  data = r.json()
  res=[]
  valid=['py','js','html','css']
  for i in data:
      if i['type']=='file':
        if i['name'].split('.')[-1] in valid:
          res += [i['url']]
      if i['type'] == 'dir':
        res += assets(i['url'])
  return res 

def res(url):
  res=url.split('github.com')[-1]
  URL = "https://api.github.com/repos"+res+"/contents"
  master={}
  for i in assets(URL):
    for j in read(i).split('\n'):
      master[j.strip()]='0'
  return master

def Compare(url1,url2):
  repo1=res(url1)
  repo2=res(url2)
  matched=0
  for i in repo1:
    if i in repo2:
      matched+=1
  for i in repo2:
    if i in repo1:
      matched+=1
  total=len(repo1)+len(repo2)
  return { 'score' : matched/total }
  
def Rate():
  URL = "https://api.github.com/rate_limit"
  r = requests.get(url = URL,auth=Headers)
  data = r.json()
  return data 
