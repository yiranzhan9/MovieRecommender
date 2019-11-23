import mysql.connector
conn = mysql.connector.connect(user='root',
                               password='ThisIsASecurePassword1313',
                               host='localhost',
                               database='MovieRecommender')
cursor = conn.cursor()
cursor.execute('INSERT INTO Movie (Title, Year,Description) VALUES ("The Thing",1982,"A research team in Antarctica is hunted by a shape-shifting alien that assumes the appearance of its victims.")')
cursor.execute('INSERT INTO Director (FirstName, LastName) VALUES ("John","Carpenter")')
cursor.execute("SELECT * FROM Movie")
for movie in cursor:
    print(movie)
cursor.execute("SELECT max(movieId) FROM Movie")
movieId = cursor.fetchall()[0][0]
cursor.execute("SELECT max(directorId) FROM Director")
directorId = cursor.fetchall()[0][0]
cursor.execute('INSERT INTO GenreToMovie (MovieId,Genre) VALUES ("'+str(movieId)+'","Horror")')
cursor.execute('INSERT INTO GenreToMovie (MovieId,Genre) VALUES ("'+str(movieId)+'","Mystery")')
cursor.execute('INSERT INTO GenreToMovie (MovieId,Genre) VALUES ("'+str(movieId)+'","Sci-Fi")')
cursor.execute('INSERT INTO DirectorToMovie (DirectorId,MovieId) VALUES ("'+str(directorId)+'","'+str(movieId)+'")')

cursor.execute('INSERT INTO Movie (Title, Year,Description) VALUES ("The Thing",2011,"At an Antarctica research site, the discovery of an alien craft leads to a confrontation between graduate student Kate Lloyd and scientist Dr. Sander Halvorson.")')
cursor.execute('INSERT INTO Director (FirstName, LastName) VALUES ("Matthijs van","Heijningen")')
cursor.execute("SELECT max(movieId) FROM Movie")
movieId = cursor.fetchall()[0][0]
cursor.execute("SELECT max(directorId) FROM Director")
directorId = cursor.fetchall()[0][0]
cursor.execute('INSERT INTO GenreToMovie (MovieId,Genre) VALUES ("'+str(movieId)+'","Horror")')
cursor.execute('INSERT INTO GenreToMovie (MovieId,Genre) VALUES ("'+str(movieId)+'","Mystery")')
cursor.execute('INSERT INTO GenreToMovie (MovieId,Genre) VALUES ("'+str(movieId)+'","Sci-Fi")')
cursor.execute('INSERT INTO DirectorToMovie (DirectorId,MovieId) VALUES ("'+str(directorId)+'","'+str(movieId)+'")')
cursor.execute("SELECT * FROM Movie")
for movie in cursor:
    print(movie)
cursor.execute("SELECT * FROM GenreToMovie")
for movie in cursor:
    print(movie)
conn.commit()
conn.close()
