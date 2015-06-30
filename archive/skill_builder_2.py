# -*- coding: utf-8 -*-
"""
Created on Mon Jun 01 23:52:19 2015

Author: Andrew
"""

import sqlite3  # import the sqlite library
import csv      # import the library that allows you to quickly process CSV files

################################################################################
################################################################################
##############     Establish Connection to the Database     ####################
################################################################################
################################################################################
# the following command establishes a connection to an existing database
# or creates one if it doesn't exist
conn = sqlite3.connect('myTunes.db')

# to manipulate the data within the database, you establish a cursor
# (something that allows you to work within the connection)
myCursor = conn.cursor()

################################################################################
################################################################################
######################     Create the database    ##############################
################################################################################
################################################################################
# get rid of a datatable if it already exists
# the most basic of approaches
myCursor.execute("DROP TABLE IF EXISTS tblArtists")
#create a table that holds the name of artists
myCursor.execute("CREATE TABLE tblArtists (ArtistName varchar, MusicGenre varchar);")

# create a table that holds the name of albums
# slighly more elegant way of creating tables
myCursor.execute("DROP TABLE IF EXISTS tblAlbums")
sqlString = """
            CREATE TABLE tblAlbums
            (Artist varchar,
             AlbumName varchar,
             ReleaseYear integer);
            """
myCursor.execute(sqlString)

# create a table that holds the name of songs
# an even more elegant way of creating a table.  Instead of deleting it and
# and rebuilding it, we only create it if it doesn't already exist.
sqlString = """
            CREATE TABLE IF NOT EXISTS tblSongs
            (AlbumName varchar,
             SongTitle varchar);
            """
myCursor.execute(sqlString)

################################################################################
################################################################################
#######################    Populate the database   #############################
################################################################################
################################################################################
# add artists one by one to table.  This is a pretty laborious process.
# This would be unmanageable given a large data set
myCursor.execute("INSERT INTO tblArtists VALUES('Aerosmith', 'Rock')")
myCursor.execute("INSERT INTO tblArtists VALUES('AC/DC', 'Rock')")
myCursor.execute("INSERT INTO tblArtists VALUES('George Strait', 'Country')")
myCursor.execute("INSERT INTO tblArtists VALUES('ABBA', 'Painful')")

# add albums using the execute many command.  This is a little more manageable
# But still unacceptable for very large data sets.
albums = (('ABBA', 'ABBA Gold Greatest Hits', 1992),
           ('ABBA', 'Waterloo', 1974),
           ('Aerosmith', 'Rocks', 1976),
           ('Aerosmith', 'Toys in the Attic', 1975),
           ('Aerosmith', 'Pump', 1989),
           ('AC/DC', 'Back in Black', 1980)
         )
myCursor.executemany("INSERT INTO tblAlbums VALUES(?, ?, ?)", albums)

# add songs by reading data from a file.  This is generally the way you want to do it.
# This approach separates data from the module and scales very nicely to large data sets.
# Notice there is no additional typing required regardless of the number of lines in the data file.
songs = []  #create the list that will contain the songs
# open the file we will read by passing the full path and indicating we only want to
# 'read a text file' (that is what the 'rt') indicates.  There are other options
myFile = open('SongList.txt', 'rt')
myReader = csv.reader(myFile)
for row in myReader:
    # remove leading and trailing spaces of each record with the strip() command
    # and append the tuple to the list (we are saving the records as a tuple)
    songs.append((row[1].strip(), row[0].strip()))
myFile.close()  # close the file

# Because we only create the table if it is missing, it is possible this table
# already exists and has data in it.  If we wrote directly into the table,
# this could result in the same record entered more than once (this is bad).
# To prevent this, we just clear the data table of any existing data by running
# a delete query and then load the entire data set again.
myCursor.execute("DELETE FROM tblSongs")
myCursor.executemany("INSERT INTO tblSongs VALUES(?, ?)", songs)

# make sure all changes (deletions and additions) are committed to the data base
conn.commit()


################################################################################
################################################################################
#######################       Use the database     #############################
################################################################################
################################################################################
# Write a simple SQL statement that SELECTs all artists from the tblArtist
# Format is "SELECT fieldname(s) FROM table name"
# Look at the sqlIte tutorial online for more information on SELECT statements
sqlString = "SELECT ArtistName FROM tblArtists"
myCursor.execute(sqlString)

# fetchall() is how you get the results from the query
b = myCursor.fetchall()
# you get to each data element by iterating through the result
for row in b:
    print row[0]

print '\n\n'    #this just adds two empty lines between query results

# Sometimes you might have the same data element appear in a data set.  You don't
# want every instance of that data element, you just need it once.  Use the distinct
# Statement if you have this kind of situation.
#Write a simple select statement using DISTINCT
sqlString = "SELECT DISTINCT Artist FROM tblAlbums"
myCursor.execute(sqlString)
b = myCursor.fetchall()
for row in b:
    print row[0]

print '\n\n'

# Sometimes you are interested in a sub set of data.  Use the where claus to define
# the sub set of data you need to access.  WHERE Clauses always come after the
# SELECT AND FROM sections of the SQL statement.
#write a simple query using the where claus
sqlString = """
            SELECT SongTitle
            FROM tblSongs
            WHERE AlbumName = 'Pump'
            """
myCursor.execute(sqlString)
b = myCursor.fetchall()
for row in b:
    print row[0]

print '\n\n'


# Sometimes the data you need is split across several tables.  In that case you
# need to combine the tables together using a "JOIN" statement.  The example
# below joins data across two tables keying on artist name.  Notice how this time
# Instead of returning only a single result we are returning two data elements
# write a query using a Join Statement
sqlString = """
            SELECT a.ArtistName, b.AlbumName
            FROM tblArtists as a JOIN tblAlbums as b ON a.ArtistName = b.Artist
            WHERE a.MusicGenre != 'Painful'
            """
myCursor.execute(sqlString)
b = myCursor.fetchall()
for row in b:
    # because we are returning two data elements, we want to access them seperately
    # we do this by directly referencing the element number of the list
    print row[0], row[1]

print '\n\n'

# Sometimes your data is scattered across more than one table.  In this instance
# you will need to write a compound joint statement that combines multiple tables
# Here we combine three tables but only pull data from two of them.
# write a query with a compound join
sqlString = """
            SELECT a.ArtistName, c.SongTitle
            FROM tblArtists as a JOIN tblAlbums as b on a.ArtistName = b.Artist
            JOIN tblSongs as c ON b.AlbumName = c.AlbumName
            WHERE a.MusicGenre != 'Painful'
            """
myCursor.execute(sqlString)
b = myCursor.fetchall()
for row in b:
    print row[0], row[1]
print '\n\n'


# Printing out data to the screen is good to let you know that you got the SQL
# statement correct.  But output to the screen is pretty useless.  You can load
# your output to a list (which is what the variable "b" is in the above examples)
# but that is only useful if you know you will need to access every record that is
# returned in a non-specific order.  Sometimes, however, you will only want a
# subset of the data for a particular task.  In that case, a dictionary will be
# very useful. In the following example, we load the data into a dictionary
mySongs = {}    # create the dictionary that will hold the songs
for row in b:
    if row[0] not in mySongs:       # check to see if the key already exists
        mySongs[row[0]]=[]          # if not, then create the key with an empty list
    mySongs[row[0]].append(row[1])  # append the current song to the list

print mySongs   #output it so you can see what the Dictionary looks like

################################################################################
################################################################################
#####################      Clean Up the database    ############################
################################################################################
################################################################################
#clean up any deleted objects
conn.execute("VACUUM")

#close the cursor
myCursor.close()

#close the connection
conn.close()
