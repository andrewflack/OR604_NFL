# -*- coding: utf-8 -*-
"""
Created on Sun May 31 20:54:49 2015

Author: Andrew

Create NFL_scheduling database, create and populate announced_games, team_info, 
and stadium_blocks tables.
"""

import sqlite3
import csv

myConnection = sqlite3.connect('NFL_scheduling.db')
myCursor = myConnection.cursor()

### Create announced_games table
sqlString = """
            CREATE TABLE IF NOT EXISTS announced_games
            (away_team char,
             home_team char);
            """
myCursor.execute(sqlString)

### Create team_info table
sqlString = """
            CREATE TABLE IF NOT EXISTS team_info
            (team char,
             conference char,
             division char,
             tz int);
            """
myCursor.execute(sqlString)

### Create stadium_blocks table
sqlString = """
            CREATE TABLE IF NOT EXISTS stadium_blocks
            (team char,
             week int,
             blocked_loc char,
             blocked_time_slot char,
             soft_const_flag int);
            """
myCursor.execute(sqlString)

### Create the slot_priority, week_priority, and team_priority tables
sqlString = """
            CREATE TABLE IF NOT EXISTS slot_priority
            (slot char,
             slot_score int);
            """
myCursor.execute(sqlString)

sqlString = """
            CREATE TABLE IF NOT EXISTS week_priority
            (week int,
             week_score int);
            """
myCursor.execute(sqlString)

sqlString = """
            CREATE TABLE IF NOT EXISTS team_priority
            (team char,
             team_score int);
            """
myCursor.execute(sqlString)

### Populate announced_games table
myFile = open('announced_games.csv', 'rt')
myReader = csv.reader(myFile)

games = []
for row in myReader:
       games.append((row[0].strip(), row[1].strip()))
myFile.close()

myCursor.execute("DELETE FROM announced_games")
myCursor.executemany("INSERT INTO announced_games VALUES(?, ?)", games)

### Populate team_info table
myFile = open('team_information.csv', 'rt')
myReader = csv.reader(myFile)

teams = []
for row in myReader:
       teams.append((row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip()))
myFile.close()

myCursor.execute("DELETE FROM team_info")
myCursor.executemany("INSERT INTO team_info VALUES(?, ?, ?, ?)", teams)

### Populate stadium_blocks table
myFile = open('stadium_blocks.csv', 'rt')
myReader = csv.reader(myFile)

blocks = []
for row in myReader:
       blocks.append((row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip(), row[4].strip()))
myFile.close()

myCursor.execute("DELETE FROM stadium_blocks")
myCursor.executemany("INSERT INTO stadium_blocks VALUES(?, ?, ?, ?, ?)", blocks)

### Populate the slot, week, and team priority tables to use as a ratings proxy
myFile = open('slot_priority.csv', 'rt')
myReader = csv.reader(myFile)

slot_priorities = []
for row in myReader:
    slot_priorities.append((row[0].strip(), row[1].strip()))
myFile.close()

myCursor.execute("DELETE FROM slot_priority")
myCursor.executemany("INSERT INTO slot_priority VALUES(?, ?)", slot_priorities)

myFile = open('week_priority.csv', 'rt')
myReader = csv.reader(myFile)

week_priorities = []
for row in myReader:
    week_priorities.append((row[0].strip(), row[1].strip()))
myFile.close()

myCursor.execute("DELETE FROM week_priority")
myCursor.executemany("INSERT INTO week_priority VALUES(?, ?)", week_priorities)

myFile = open('team_priority.csv', 'rt')
myReader = csv.reader(myFile)

team_priorities = []
for row in myReader:
    team_priorities.append((row[0].strip(), row[1].strip()))
myFile.close()

myCursor.execute("DELETE FROM team_priority")
myCursor.executemany("INSERT INTO team_priority VALUES(?, ?)", team_priorities)

### Commit all changes to the database
myConnection.commit()

### Close the cursor and connection
myCursor.close()
myConnection.close()