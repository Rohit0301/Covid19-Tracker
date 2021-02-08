from django.shortcuts import render,redirect, HttpResponse
import requests
import json
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
    params = {
        "ss": lst,
        "ind": lst[-1],
        "date": data["TT"]["meta"]["tested"]["last_updated"]
    }
    return render(request, 'state.html', params)



def DistrictWise(request):
    parms = {

        "data1": district(),
    }

    return render(request, 'home.html', parms)

