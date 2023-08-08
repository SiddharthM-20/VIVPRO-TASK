'''
VIVPRO TAKE HOME EXERCISE


TASK-1
DATA PROCESSING
'''

import json
import sqlite3

#IMPORTING JSON FILE AND EXTRACTING DATA
fname = 'playlist.json'
fhand = open(fname,'r')
data = fhand.read()

#DECODING JSON TO PYTHON DICTIONARY
data = json.loads(data)
tab_head = list(data.keys())
index = list(data[tab_head[0]])


#CREATING SQLITE DATABASE OF PLAYLIST SONGS
try:
    conn = sqlite3.connect('songs.sqlite')
    cursor = conn.cursor()
    print("Connection with database established!")
except:
    print("Error in database connection")
    quit()

#DELETE ANY PRE-EXISTING TABLE
cursor.execute("DROP TABLE IF EXISTS playlist")
conn.commit()
print("Deleted any pre-existing table playlist to avoid redundancy of data!")

#CREATING TABLE PLAYLIST IN SONGS DATABASE
sql_query = """ CREATE TABLE IF NOT EXISTS playlist (
                idx INT PRIMARY KEY,
                id TEXT NOT NULL,
                title TEXT NOT NULL,
                danceability DOUBLE NOT NULL,
                energy DOUBLE NOT NULL,
                key INT NOT NULL,
                loudness DOUBLE NOT NULL,
                mode INT NOT NULL,
                acousticness DOUBLE NOT NULL,
                instrumentalness DOUBLE NOT NULL,
                liveness DOUBLE NOT NULL,
                valence DOUBLE NOT NULL,
                tempo DOUBLE NOT NULL,
                duration_ms INT NOT NULL,
                time_signature INT NOT NULL,
                num_bars INT NOT NULL,
                num_sections INT NOT NULL,
                num_segments INT NOT NULL,
                class INT NOT NULL
)"""

cursor.execute(sql_query)
print("Playlist table is created!")

#INSERTING DATA
print("Inserting data into playlist table! Please wait...")
for i in range(len(index)):
    query = " INSERT INTO playlist VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    param = (i,)+tuple(data[tab_head[j]][index[i]] for j in range(len(tab_head)))
    cursor.execute(query, param)
    conn.commit()

print("Done, playlist table is ready to use!")

conn.close()