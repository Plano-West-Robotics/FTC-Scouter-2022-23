 #ALL IMPORTS
from pathlib import Path
import requests
import re
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

headers = {'accept':'application/json', 'Authorization': 'Basic c2FrZXRoZ246MjlFRTFFQTQtRTU4RS00MjNDLUI4OUUtQTVCOUZDQ0VDQjAy'}

#Set up tournament code to whatever the current tournament is
tournamentCode = 'USTXNOTLM3'
numLookup = 3
allTeams = []

req = requests.get("http://ftc-api.firstinspires.org/v2.0/{season}/teams".format(season = "2022"), headers = headers, params={'eventCode':tournamentCode})
allTeams = re.findall(r'(?:"teamNumber":)(.*?)(?:,"nameFull)', req.text)
print(allTeams)

def sortDateList(allEvents, dates):
    dateList = []
    combinedData = []
    for x in dates:
        date, sep, time = x.partition('T')
        dateList.append(date)
    
    for num in range(len(allEvents)):
        combinedData.append([allEvents[num], dateList[num]])
    finalList = []
    #print(combinedList)
    combinedData.sort(key=lambda date: datetime.strptime(date[1], "%Y-%m-%d"))
    for element in combinedData:
        finalList.append(element[0])
    return finalList

allData = []
for teamNumber in allTeams:
  redMatchCount = 0
  blueMatchCount = 0
  allMatchesPrePenaltyScores = []
  #parkingCount = 0
  highestConeCount = 0
  redAutonChance = [0]*25
  blueAutonChance = [0]*25
  redAutoConeData = [0]*25
  blueAutoConeData = [0]*25
  redDCConeData = [0]*25
  blueDCConeData = [0]*25
  numConesPlaced = 0
  penaltyCount = 0
  penaltyScore = 0
  circuitCount = 0
  prePenaltyScoreAll = 0
  autonScore = 0
  numMatches = 0
  avgOwnedJunctions = 0
  sep = 'T'
  numMatches = 0

  #Basic Data
  req = requests.get("http://ftc-api.firstinspires.org/v2.0/{season}/teams".format(season = "2022"), headers = headers, params={'teamNumber':teamNumber})
  teamName = re.findall(r'(?:"nameShort":")(.*?)(?:","schoolName")', req.text)[0]
  teamSchool = re.findall(r'(?:"nameFull":")(.*?)(?:","nameShort")', req.text)[0]
  teamData = {'teamNumber': teamNumber, 'teamName': teamName, 'teamSchool': teamSchool}
  req = requests.get("https://ftc-api.firstinspires.org/v2.0/2022/events", headers=headers, params={'teamNumber': teamNumber})

  #Orders the events into order
  allEventsList = re.findall(r'code":"(.*?)","divisionCode', req.text)
  dates = re.findall(r'"dateStart":"(.*?)","dateEnd"', req.text)
  allEventsList = sortDateList(allEventsList, dates)

  #Removes events that don't have data(haven't happened yet)
  tempList = allEventsList.copy()
  for anEvent in tempList:
    req = requests.get("http://ftc-api.firstinspires.org/v2.0/2022/matches/{tournament}".format(tournament = anEvent), headers = headers, params={'teamNumber':teamNumber})
    if(req.text == '{"matches":[]}'):
      allEventsList.remove(anEvent)

  #Makes sure that the list's length is equal to or less than the number of tournaments attended
  if(len(allEventsList) > numLookup):
    tempList = allEventsList[-1:(-1*(1 + numLookup)):-1]
    allEventsList = tempList

  for eventCode in allEventsList:
    matchIndex = 0
    req = requests.get("http://ftc-api.firstinspires.org/v2.0/2022/matches/{tournament}".format(tournament = eventCode), headers = headers, params={'teamNumber':teamNumber})
    teamColor = re.findall(r'(?:{teamNumber},"station":")(.*?)(?:","dq")'.format(teamNumber = teamNumber), req.text)
    for color in teamColor:
        if(color[:-1] == 'Red'):
            redMatchCount += 1
        elif(color[:-1] == 'Blue'):
            blueMatchCount += 1
    req = requests.get("http://ftc-api.firstinspires.org/v2.0/{season}/scores/{eventCode}/{tournamentLevel}".format(season = 2022, eventCode = eventCode, tournamentLevel = 'qual'), headers=headers, params={'teamNumber': teamNumber})
    allMatchesData = req.text
    individualMatchList = re.findall(r'(?:"matchLevel":)(.*?)(?:}]})', allMatchesData)

    #This means they made it to playoffs, so adds those teams to it
    if(len(teamColor) > len(individualMatchList)):
      req = requests.get("http://ftc-api.firstinspires.org/v2.0/{season}/scores/{eventCode}/{tournamentLevel}".format(season = 2022, eventCode = eventCode, tournamentLevel = 'playoff'), headers=headers, params={'teamNumber': teamNumber})
      allMatchesData = req.text
      matchList = re.findall(r'(?:"matchLevel":)(.*?)(?:}]})', allMatchesData)
      for aMatch in matchList:
        individualMatchList.append(aMatch)
    for match in individualMatchList:
      numMatches += 1
      rightData = re.findall(r'(?:"alliance":"{teamColor}")(.*?)(?:"totalPoints")'.format(teamColor = teamColor[matchIndex][:-1]), match)


      ownedJunctionsCount = (re.findall(r'(?:"ownedJunctions":)(.*?)(?:,"circuit":)', rightData[0]))[0]
      avgOwnedJunctions += int(ownedJunctionsCount)

      circuitOrNo = (re.findall(r'(?:circuit":)(.*?)(?:,)', rightData[0]))[0]

      prePenaltyScoreAll += int(re.findall(r'(?:"prePenaltyTotal":)(.*?)(?:,"autoJunctionCones")', rightData[0])[0])
      allMatchesPrePenaltyScores.append(int(re.findall(r'(?:"prePenaltyTotal":)(.*?)(?:,"autoJunctionCones")', rightData[0])[0]))

      if circuitOrNo == 'true':
          circuitCount += 1

      autonScore += int(re.findall(r'(?:"autoPoints":)(.*?)(?:,"dcPoints")', rightData[0])[0])
      autoConeList = re.findall(r'(?:"autoJunctions":)(.*?)(?:,"dcJunctions":)', rightData[0])
      autoConeList = eval(autoConeList[0])

      coneIndex = 0
      count = 0
      maxCone = 0
      for row in autoConeList:
          for col in row:
              count = 0
              for item in col:
                  if item == 'MY_CONE' or item == 'MY_R{number}_BEACON'.format(number = teamColor[matchIndex][len(teamColor[matchIndex]) - 1]):
                      count += 1                        
              if teamColor[matchIndex][:-1] == "Red": 
                  redAutoConeData[coneIndex] += count
              elif teamColor[matchIndex][:-1] == "Blue":
                  blueAutoConeData[coneIndex] += count
              else:
                  print("COULDNT DETECT CONE DATA. SOMETHING WENT VERY WRONG")
              count = 0
              coneIndex += 1

      coneIndex = 0
      count = 0
      for row in autoConeList:
          for col in row:
              count = 0
              for item in col:
                  if item == 'MY_CONE' or item == 'MY_R{number}_BEACON'.format(number = teamColor[matchIndex][len(teamColor[matchIndex]) - 1]):
                      count += 1                        
              if teamColor[matchIndex][:-1] == "Red": 
                if count >= 1:
                  redAutonChance[coneIndex] += 1
              elif teamColor[matchIndex][:-1] == "Blue":
                if count >= 1:
                  blueAutonChance[coneIndex] += 1
              else:
                  print("COULDNT DETECT CONE DATA. SOMETHING WENT VERY WRONG")
              count = 0
              coneIndex += 1

      dcConeList = re.findall(r'(?:"dcJunctions":)(.*?)(?:,"dcTerminalNear")', rightData[0])                
      dcConeList = eval(dcConeList[0])       
      coneIndex = 0
      count = 0
      for row in dcConeList:
          for col in row:
              count = 0
              for item in col:
                  if item == 'MY_CONE' or item == 'MY_R{number}_BEACON'.format(number = teamColor[matchIndex][len(teamColor[matchIndex]) - 1]):
                      count += 1
              if teamColor[matchIndex][:-1] == "Red": 
                  redDCConeData[coneIndex] += count
              elif teamColor[matchIndex][:-1] == "Blue":
                  blueDCConeData[coneIndex] += count
              else:
                  print("COULDNT DETECT CONE DATA. SOMETHING WENT VERY WRONG")
              if count > maxCone:
                maxCone = count
              count = 0
              coneIndex += 1
      highestConeCount += maxCone
      penaltyVal = re.findall(r'(?:"penaltyPointsCommitted":)(.*?)(,"prePenaltyTotal")', rightData[0])
      penaltyScore += int(penaltyVal[0][0])
      
      if(int(penaltyVal[0][0]) > 0):
          penaltyCount += 1

      matchIndex += 1
  redAutoSum = sum(redAutoConeData)
  if(redAutoSum > 0):
    redAutoFinalData = []
    for val in redAutoConeData:
      redAutoFinalData.append(val/(redMatchCount))

  redDCSum = sum(redDCConeData)
  redDCFinalData = [] 
  if(redDCSum > 0):
    redDCFinalData = []
    for val in redDCConeData:
      redDCFinalData.append(val/(numMatches/2))

  blueAutoSum = sum(blueAutoConeData)
  if(blueAutoSum > 0):
    blueAutoFinalData = []
    for val in blueAutoConeData:
      blueAutoFinalData.append(val/(blueMatchCount))

  blueDCSum = sum(blueDCConeData)
  blueDCFinalData = []
  if(blueDCSum > 0):
    for val in blueDCConeData:
      blueDCFinalData.append(val/(numMatches/2))
  
  for num in range(len(redAutonChance)):
    redAutonChance[num] = redAutonChance[num]/redMatchCount

  for num in range(len(blueAutonChance)):
    blueAutonChance[num] = blueAutonChance[num]/blueMatchCount
  
  for num in range(len(redAutonChance)):
    if redAutonChance[num] < 0.6:
      redAutoFinalData[num] = 0
  
  for num in range(len(blueAutonChance)):
    if blueAutonChance[num] < 0.6:
      blueAutoFinalData[num] = 0
  robotType = ""
  if circuitCount/numMatches > 0.25:
    robotType = "circuit"
  elif((max(redDCFinalData) + max(blueDCFinalData) / 2) > 0.4):
    robotType = "stacker"  
  else:
    robotType = "unknown"
  
  teamData['numMatches'] = numMatches
  teamData['averageScore'] = round(prePenaltyScoreAll/numMatches, 2)
  teamData['circuitChance'] = (round(circuitCount/numMatches, 2) * 100)
  teamData['averageAutonScore'] = round(autonScore/numMatches, 2)
  teamData['robotType'] = robotType
  teamData['ListOfAverageScores'] = allMatchesPrePenaltyScores
  teamData['averagePenaltyScore'] = round(penaltyScore/penaltyCount, 2)
  teamData['averagePenaltyChance'] = (round(penaltyCount/numMatches, 2) * 100)
  print("Team Number: " + str(teamData['teamNumber']))
  allData.append(teamData)

with open("allScoutingData.txt", mode = "w") as f:
  f.write(str(allData))