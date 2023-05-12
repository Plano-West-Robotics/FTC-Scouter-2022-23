import matplotlib.pyplot as plt
import numpy as np

class ScoutingDisplay:
    def __init__(self):
        file = open("allScoutingData.txt", mode = "r")
        self.allData = eval(file.read())
        file.close()
    def printTeamStats(self, teamNumber):
        for teamData in allData:
            if(teamData['teamNumber'] == str(teamNumber)):
                print("Team Number: " + str(teamData['teamNumber']))
                print("Team Name: " + teamData['teamName'])
                print("School/Organization: " + teamData['teamSchool'])
                print('\n')
                print("OVERALL DATA")
                plt.boxplot(teamData['ListOfAverageScores'], patch_artist = True, vert = 0)
                plt.title(str(teamNumber) + "'s scores")
                plt.show()
                print("Average Score: " + str(teamData['averageScore']))
                print("Chance of a circuit " + str(teamData['circuitChance']))
                print("Robot Type: " + str(teamData['robotType']))
                print("Penalty Chance: " + str(teamData['averagePenaltyChance']))
                print("Average Penalty Score(When they got a penalty, what was the average score?): " + str(teamData['averagePenaltyScore']))
                print("Average Autonomous Score: " + str(teamData['averageAutonScore']))
                print('\n\n')
    def printMultipleTeamStats(self, listOfTeams):
        for team in listOfTeams:
            self.printTeamStats(team)
    def printAllAverageScoresGraphAscending(self):
        newList = sorted(allData, key=lambda team: team['averageScore'])
        allGraphs = []
        allTeams = []
        for team in newList:
            allGraphs.append(team['ListOfAverageScores'])
            allTeams.append(team['teamNumber'])
        fig = plt.figure(figsize =(20, 14))
        ax = fig.add_subplot(111)
        bp = ax.boxplot(allGraphs, patch_artist = True, vert = 0)
        ax.set_yticklabels(allTeams)
        plt.title("Team Scores")
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        plt.show()