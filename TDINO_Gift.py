#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 11:18:33 2021

@author: danielgift
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime
from tabulate import tabulate
#List of file names
fileNames = [
            "Calls_for_Service_2016.csv",
            "Calls_for_Service_2017.csv",
            "Calls_for_Service_2018.csv",
            "Calls_for_Service_2019.csv",
            "Call_for_Service_2020.csv"
            ]
#Question 1
data2020 = pd.read_csv(fileNames[-1])
numCalls = len(data2020)
mostFreqTypeNum = data2020.Type.value_counts().values[0]
print("Fraction of calls of the most common type: ", mostFreqTypeNum/numCalls)

#Question 2
calltypes2020 = data2020.filter(["TypeText","Type"]).groupby(
    "TypeText").count().rename(columns={"Type":"2020count"})
data2016 = pd.read_csv(fileNames[0])
calltypes2016 = data2016.filter(["TypeText","Priority"]).groupby(
    "TypeText").count().rename(columns={"Priority":"2016count"})
calltypesBoth = calltypes2020.join(calltypes2016,on="TypeText")
#Column for the number fewer cases in 2020 than 2016
calltypesBoth["Decrease"] = calltypesBoth["2016count"]-calltypesBoth["2020count"]
#Decrease as a fraction of 2016 count
calltypesBoth["PercentDecrease"] = calltypesBoth["Decrease"]/calltypesBoth["2016count"]
print("Largest percentage decrease betweeon 2016 and 2020: ",
      max(calltypesBoth["PercentDecrease"].values))

#Question 3
totalData = pd.DataFrame()
numDropped = 0
for file in fileNames:
    newDF = pd.read_csv(file,low_memory=False)
    print(newDF.columns)
    newDF = newDF.rename(columns={"TimeArrival":"TimeArrive"})
    if len(totalData) == 0:
        totalData = newDF
    else:
        totalData = totalData.append(newDF)
oldLen = len(totalData)
#Drop the duplicates
totalData = totalData.drop_duplicates(subset="NOPD_Item")
newLen = len(totalData)
print("Number of dropped duplicates: ", oldLen-newLen)

#Question 4
timeDispatch = [] #Array to store dispatch times
#Function to parse date and time
def parsetime(dt):
    [date, time, AMPM] = dt.split(" ")
    [month,day,year] = date.split("/")
    [hour,minute,second] = time.split(":")
    hour = int(hour)
    if AMPM == "PM" and hour < 12:
        hour += 12
    if AMPM =="AM" and hour == 12:
        hour -= 12
    return (datetime(int(year),int(month),int(day),int(hour),int(minute),int(second)))
for t in totalData["TimeDispatch"].values:
    if type(t) != float:
        timeDispatch.append(parsetime(t))
    else: #Use default "absurd" value for invalid values
        timeDispatch.append(parsetime("01/01/1900 00:00:01 AM"))
timeDispatch= np.array(timeDispatch)
timeArrived = [] #Array to store arrival times
for t in totalData["TimeArrive"].values:
    if type(t) != float:
        timeArrived.append(parsetime(t))
    else: #Use default "absurd" value for invalid values
        timeArrived.append(parsetime("01/01/1900 00:00:00 AM"))
timeArrived = np.array(timeArrived)
responseTime = []
for i in range(len(timeArrived)):
    responseTime.append((timeArrived[i] - timeDispatch[i]).total_seconds())
#Make all invalid response times into NaN
ResponseTimes = [x if (x >=0 and x <1e8) else float("NaN") for x in responseTime ]
print("Median ResponseTime (s): ", np.nanmedian(ResponseTimes))

#Question 5
totalData["ResponseTime"] = ResponseTimes
responseByDistrict = totalData.groupby("PoliceDistrict")["ResponseTime"].mean()
#District 0 isn't a real district, so we exclude it
diffInAvgResponseTime = max(responseByDistrict.values[1:]) - min((responseByDistrict.values[1:]))
print("Difference between min and max Avg. Response Time: ", diffInAvgResponseTime)

#Question 6
month = [] #6 digit number prespresenting year and month
for t in totalData["TimeCreate"].values:
    monthstr, _, yearstr = t.split(" ")[0].split("/")
    month.append(int(yearstr+monthstr))
totalData["Month"] = month
responseByMonth = totalData.groupby("Month")["ResponseTime"].mean()
#X-array for months since January 2016
monthsFromJan2016 = np.arange(len(responseByMonth.values))
vals = np.polyfit(monthsFromJan2016,responseByMonth.values,1)
# plt.scatter(monthsFromJan2016,responseByMonth.values)
# def theline(x):
#     return vals[1]+x*vals[0]
# plt.plot(monthsFromJan2016,theline(monthsFromJan2016))
# plt.show()
#Slope is seconds per month, multiply by 12 to get per year
print("Average change of response time in seconds per year: ",vals[0]*12)

#Question 7
numType = totalData.filter(["NOPD_Item","TypeText"]).groupby(
    "TypeText").count().rename(columns={"NOPD_Item":"Count"})
#A list of only the types of crimes that have at least 100 reports
listBigTypes = numType[numType["Count"]>100].index
bigsOnly = totalData[totalData["TypeText"].isin(listBigTypes)]
#Make sure to exclude district 0
byDistrictAndType = pd.DataFrame(bigsOnly[bigsOnly["PoliceDistrict"]!=0].groupby(
    ["TypeText","PoliceDistrict"])["NOPD_Item"].size()).rename(columns={"NOPD_Item":"Count"})
allByDistrict = pd.DataFrame(totalData.filter(["PoliceDistrict","NOPD_Item"]).groupby(
    ["PoliceDistrict"])["NOPD_Item"].count()).rename(columns={"NOPD_Item":"Count"})
byType = pd.DataFrame(bigsOnly.filter(["TypeText","NOPD_Item"]).groupby(
    "TypeText")["NOPD_Item"].count()).rename(columns={"NOPD_Item":"Count"})
bestRatio = 0 #Keeps track of the highest ratio of liklihoods we've sen so far
for _,row in byDistrictAndType.iterrows():
    numCond = row["Count"] #Number of counts in this district of this type
    numTot = byType.loc[row.name[0],"Count"] #total number of this type
    denomCond = allByDistrict.loc[row.name[1],"Count"] #Number of reports for this district
    denomTot = len(totalData) #total number of reports
    ratio = (numCond/denomCond)/(numTot/denomTot)
    if ratio > bestRatio:
        bestRatio = ratio
print("Largest ratio of conditional probability to nonconditional probability:",bestRatio)

#Question 8
locs = totalData["Location"]
lats = [] #store latitudes of each location 
longs = [] #Store longistudes of each location
for l in locs: #Parse the location info; store as 0's if invalid
    if type(l) != str:
        lat = 0.
        long = 0.
    else:
        latsandlongs = l.split(" ")
        if len(latsandlongs) == 3:
            _,lati, longi = latsandlongs
            lat = float(lati[1:])
            long = float(longi[:-1])
            if lat > 100 or long > 32: 
                lat = 0.
                long= 0.
        else:
            longi, lati = latsandlongs
            if longi[0] == "(":
                lat = float(lati[:-1])
                long = float(longi[1:-1])
                if lat > 100 or long > 32: 
                    lat = 0.
                    long= 0.
            else:
                if longi[-1]=="E":
                    lat = 0.
                    long = 0.
                else:
                    lat = float(lati)
                    long = float(longi)
                    if lat > 100 or long > 32: 
                        lat = 0.
                        long= 0.
    lats.append(lat)
    longs.append(long)
#From https://www.johndcook.com/how_big_is_a_degree.html, with NO at 29 degrees N,
#One degree of latitude is 111 km and one degree of longistude is 96 km
deglat = 111
deglong = 59
totalData["Latitude"] = np.array(lats)
totalData["Longitude"] = np.array(longs)
xdata = pd.DataFrame(totalData[totalData["Latitude"] != 0].groupby("PoliceDistrict")["Latitude"].std())
ydata = pd.DataFrame(totalData[totalData["Longitude"] != 0].groupby("PoliceDistrict")["Longitude"].std())
areaData = xdata.join(ydata) 
#Areas of the districts
area = areaData["Latitude"].values*areaData["Longitude"].values*np.pi*deglat*deglong
#Be sure to exclude district 0
print("Area of largest district in sq. km: ",max(area[1:]))

# plt.show()

# xx=totalData[(totalData["PoliceDistrict"]==2)&(totalData["Longitude"] != 0)]["Latitude"].values
# yy=totalData[(totalData["PoliceDistrict"]==2)&(totalData["Longitude"] != 0)]["Longitude"].values
# plt.scatter(xx,yy,color='k')
# xx=totalData[(totalData["PoliceDistrict"]==3)&(totalData["Longitude"] != 0)]["Latitude"].values
# yy=totalData[(totalData["PoliceDistrict"]==3)&(totalData["Longitude"] != 0)]["Longitude"].values
# plt.scatter(xx,yy,color='y')
# xx=totalData[(totalData["PoliceDistrict"]==4)&(totalData["Longitude"] != 0)]["Latitude"].values
# yy=totalData[(totalData["PoliceDistrict"]==4)&(totalData["Longitude"] != 0)]["Longitude"].values
# plt.scatter(xx,yy,color='c')
# xx=totalData[(totalData["PoliceDistrict"]==5)&(totalData["Longitude"] != 0)]["Latitude"].values
# yy=totalData[(totalData["PoliceDistrict"]==5)&(totalData["Longitude"] != 0)]["Longitude"].values
# plt.scatter(xx,yy,color='m')
# xx=totalData[(totalData["PoliceDistrict"]==6)&(totalData["Longitude"] != 0)]["Latitude"].values
# yy=totalData[(totalData["PoliceDistrict"]==6)&(totalData["Longitude"] != 0)]["Longitude"].values
# plt.scatter(xx,yy,color='b')
# xx=totalData[(totalData["PoliceDistrict"]==7)&(totalData["Longitude"] != 0)]["Latitude"].values
# yy=totalData[(totalData["PoliceDistrict"]==7)&(totalData["Longitude"] != 0)]["Longitude"].values
# plt.scatter(xx,yy,color='g')
# xx=totalData[(totalData["PoliceDistrict"]==8)&(totalData["Longitude"] != 0)]["Latitude"].values
# yy=totalData[(totalData["PoliceDistrict"]==8)&(totalData["Longitude"] != 0)]["Longitude"].values
# plt.scatter(xx,yy,color='orange')
# xx=totalData[(totalData["PoliceDistrict"]==1)&(totalData["Longitude"] != 0)]["Latitude"].values
# yy=totalData[(totalData["PoliceDistrict"]==1)&(totalData["Longitude"] != 0)]["Longitude"].values
# plt.scatter(xx,yy,color='r')
# xx=totalData[(totalData["PoliceDistrict"]==0)&(totalData["Longitude"] != 0)]["Latitude"].values
# yy=totalData[(totalData["PoliceDistrict"]==0)&(totalData["Longitude"] != 0)]["Longitude"].values
# plt.scatter(xx,yy)
# plt.show()
    
    