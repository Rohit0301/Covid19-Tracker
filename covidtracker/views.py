from django.shortcuts import render,redirect, HttpResponse
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
now = datetime.now()

def district():
    api="https://api.covid19india.org/v2/state_district_wise.json"

    s=(requests.get(api)).text

    data=json.loads(s)
    return data

def stateWise(request):
    api = "https://api.covid19india.org/v4/data.json"
    s = (requests.get(api)).text
    data = json.loads(s)
    statelist = ["Andaman and Nicobar Islands", "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chandigarh",
                 "Chattisgarh",
                  "Delhi", "Dadar and Nagar Havelli", "Goa", "Gujarat", "Haryana", "Himachal Pradesh",
                 "Jammu and Kashmir", "jharkhand", "Karnataka", "Kerala", "Ladakh",  "Madhya Pradesh",
                 "Maharashtra",
                 "Manipur", "Meghalya", "Mizoram", "Nagaland", "Orissa", "Punjab", "Pondicherry", "Rajastha", "Sikkim",
                 "Tamil Nadu",
                 "Telangana", "Tripura", "Uttarakhand", "Uttar Pradesh", "West Bengal","Total"]
    statecode = ["an", "ap", "ar", "as", "br", "ch", "ct",  "dl", "dn", "ga", "gj", "hr", "hp", "jk", "jh", "ka",
                 "kl", "la",
                 "mp", "mh", "mn", "ml", "mz", "nl", "or", "pb", "py", "rj", "sk", "tn", "tg", "tr", "ut", "up", "wb"
                ,"tt"]
    lst = []
    for i in range(len(statecode)):
        dict = {}
        l = data[statecode[i].upper()]
        dict["state"] = statelist[i]
        if "delta" in l.keys():
            dict["daily"] = l["delta"]
        else:
            dict["daily"] = {"confirmed": 0,
          "deceased": 0,
          "recovered": 0,
          "tested": 0}
        dict["total"] = l["total"]
        lst.append(dict)
    dt=data["TT"]["meta"]["tested"]["last_updated"]     
    params = {
        "ss": lst,
        "ind": lst[-1],
        "date": date(dt)
    }
    return render(request, 'state.html', params)
      

def date(date):
  ls=date.split('-')
  monthName=None
  mon=['ind','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']
  if(ls[1][0]=='0'):
    monthName=mon[int(ls[1][1])]
  else:
    monthName=mon[int(ls[1])]

  return (ls[2]+' '+monthName+' '+ls[0])   


def DistrictWise(request):
    ls=district()
    ls.pop(0)
    parms = {

        "data1": ls,
    }

    return render(request, 'home.html', parms)


def apiforindia():
    api="https://api.covid19india.org/data.json"
    s=(requests.get(api)).text
    data=json.loads(s)
    return data

def apiforworld():
    api="https://corona.lmao.ninja/v2/all"
    s=(requests.get(api)).text
    data=json.loads(s)
    return data

def country():
    api="https://corona.lmao.ninja/v2/countries#"

    s=(requests.get(api)).text

    data=json.loads(s)
    return data


def news():
    url="https://news.google.com/topics/CAAqBwgKMMqAmAsw9KmvAw?hl=en-IN&gl=IN&ceid=IN%3Aen" #google news URL for scraping it.
    q=requests.get(url)
    soup=BeautifulSoup(q.text,"html.parser")
    news_headline=soup.find_all('h3',class_="ipQwMb ekueJc RD0gLb") # News Headline
    images = soup.findAll('img',class_="tvs3Id QwxBBf") #Image links related to News-headline
    link = soup.findAll('a',class_="VDXfz") # News-Headline deatail link
    news_headline_list=[n.text for n in news_headline]
    image_link=[j['src'] for j in images]
    headline_link=["https://news.google.com/"+str(j['href']) for j in link]

    serial=1
    value=[]
    for j in range(20):
        value.append({"serial":serial,"date":now.strftime("%d %b"),"Headline":news_headline_list[j],"image_link":image_link[j],"headline_link":headline_link[j]})
        serial+=1

    # with open("google-news"+str(now.strftime(" %d%b"))+".json", 'w') as file:
    #     json.dump(value, file)
    return value

# Views START FROM HERE
def globalD(request):
    parms={
        "data1":country(),
        "data":apiforindia(),
        "data2":apiforworld(),

    }

    return render(request, 'global.html', parms)


def News(request):
    parms={
        "news":news(),
        "now":now
    }
    return render(request, 'news.html', parms)    