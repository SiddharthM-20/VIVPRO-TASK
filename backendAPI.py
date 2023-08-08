'''
VIVPRO TAKE HOME EXERCISE


TASK-2
API to Serve the Normalised Data
'''

from flask import Flask, request, jsonify, render_template
import sqlite3

#CREATING FLASK APPLICATION INSTANCE
app = Flask(__name__)

#FUNCTION TO CONNECT SQLITE DATABASE OF PLAYLIST SONGS 
def db_connect():
    try:
        conn = sqlite3.connect('songs.sqlite')
        return conn
    except:
        quit()


#FUNCTION FOR INDEX PAGE
@app.route('/', methods=["GET"])
def index():
    #TO DISPLAY DETAILS OF ALL SONG IN PLAYLIST
    conn = db_connect()
    cursor = conn.cursor()
    query = cursor.execute("SELECT * FROM playlist")
    songs = [
            dict(index=row[0], title=row[2], duration_ms=row[13])
            for row in query.fetchall()
    ]
    conn.close()
    if songs is not None:
        return jsonify(songs)
    else:
        return "Not Found!"
        

#FUNCTION FOR SEARCHING SONG BASED ON TITLE
@app.route('/search', methods=["GET", "POST"])
def title_name():

    #TO SHOW SONG DETAILS AS TITLE RECIEVED OVER FORM
    if request.method == "POST":
        conn = db_connect()
        cursor = conn.cursor()
        query = cursor.execute("SELECT * FROM playlist WHERE title IS ?", (request.form['song_title'],))
        songs = [
            dict(index = row[0],
                id = row[1],
                title = row[2],
                danceability = row[3],
                energy = row[4],
                key = row[5],
                loudness = row[6],
                mode = row[7],
                acousticness = row[8],
                instrumentalness =row[9],
                liveness = row[10],
                valence = row[11],
                tempo = row[12],
                duration_ms = row[13],
                time_signature = row[14],
                num_bars = row[15],
                num_sections = row[16],
                num_segments = row[17],
                class_ = row[18])
            for row in query.fetchall()
        ]
        conn.close()
        if len(songs)>0:
            return jsonify(songs)
        else:
            return "Not found any song with given title in playlist!"
        
    #TO DISPLAY PAGE IF "GET" REQUEST
    else:
        return render_template("search.html")


#FUNCTION FOR ADDING RATING TO THE SONGS
@app.route('/rating', methods=["GET", "POST"])
def star_rating():
    #CHECKING ALREADY PRESENT COLUMN STAR_RATING IN TABLE
    conn = db_connect()
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE playlist ADD star_rating INT")
        conn.commit()
    except:
        pass

    #TO UPDATE TABLE AS TITLE AND STAR RATING RECIEVED OVER FORM
    if request.method == "POST":
        cursor.execute("UPDATE playlist SET star_rating=? WHERE title IS ? ",(int(request.form["star_rating"]), request.form["song_title"]))
        conn.commit()
        query = cursor.execute("SELECT * FROM playlist WHERE title IS ?", (request.form['song_title'],))
        songs = [
            dict(index = row[0],
                title = row[2],
                duration_ms = row[13],
                rating = row[19])
            for row in query.fetchall()
        ]
        conn.close()
        if len(songs)>0:
            return jsonify(songs)
        else:
            return "Not found any song with given title in playlist!"

    #TO DISPLAY PAGE IF "GET" REQUEST
    else:
        conn.close()
        return render_template("rating.html")
    



#TO RUN FLASK APPLICATION
if __name__ == '__main__':
    app.run(debug=True)