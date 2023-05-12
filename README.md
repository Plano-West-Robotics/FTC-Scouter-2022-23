# FTCScouter
FTC Scouting App

This will be your guide to using the FTC Scouter
For this version of the scouter, I split it up into 2 seperate programs, one to generate the scouting data, and another to display them. This way, once the scouting data is generated, you can quickly get the necessary data from each time rather than having to rerun the script each time. 

To generate the data, download ScoutingGenerator.py into a directory of your choice, just make sure that you know which directory it is in. There are only 2 things you can change, the tournamentCode on line 12 and numLookup on line 13. Change the tournament code to whatever the current tournament is, and it will generate all the data for the teams at that tournament(If you are reading this before buc days, the tournament code is USTXCECCS. However, the teams haven't been displayed yet). numLookup refers to how many tournaments previously the scouter will look at. By default, it is set to 3 which means for each team the program scouts, it will grab data from the last 3 tournaments only. You can change this if you want, it is up to personal preference. 

Once you are satisfied with the tournamentCode and numLookup, you can run the script. It will print the team number to the console once it is done scouting a particular team, which can take between 5-10 seconds per team. After this, all the scouting data will be saved to the file allScoutingData.txt which will be located in the same directory where you ran the script. Check the directory to make sure the file was generated and that it contains the scoutingData.

Once this is done, you can use the ScoutingDisplay.py program to visually display all of these stats quickly. There are 3 functions that you can perform, print the data of one team, print the data of multiple teams, and generate a graph of average scores. You can do each of these by adding the following code to the bottom of ScoutingDisplay.py:

x = ScoutingDisplay #Creates a new Scouting Display object

x.printTeamStats(12977) #Prints the statistics of the team specified in the parameter. Keep in mind, it will only generate this if the team specified exists in the text file that is created

x.printMultipleTeamStats(listOfTeams = [12977, 14523]) #Prints the statistics of the teams specified in the parameter. Keep in mind, it will only generate this if the team specified exists in the text file that is created

x.printAllAverageScoresGraphAscending() #Arranges all the teams by ascending order of average scores and displays them on a graph

That is it. If you have any questions, message me on discord and I will respond ASAP. 
