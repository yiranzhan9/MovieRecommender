import mysql.connector
import json
import pandas

#Connect to local MySQL server
conn = mysql.connector.connect(user='root',
                               password='vhyirj981022',
                               host='localhost')
cursor = conn.cursor()
#Remove and Re-add database
cursor.execute("DROP DATABASE MovieRecommender")
cursor.execute("CREATE DATABASE MovieRecommender")
conn.close()

#Read in initial data as csv into pandas dataframs
Director = pandas.read_csv('Director.csv')
DirectorToMovie = pandas.read_csv('DirectorToMovie.csv')
Movie = pandas.read_csv('Movie.csv')
GenreToMovie = pandas.read_csv('GenreToMovie.csv')
Rating = pandas.read_csv('Rating.csv')

#Escape quotes from title and descriptions -- assume other fields will not have any
cols = ['Title','Description']
Movie[cols] = Movie[cols].replace({';': ';'}, regex=True)
Movie[cols] = Movie[cols].replace({"'": "\\'"}, regex=True)
Movie[cols] = Movie[cols].replace({'"': '\\"'}, regex=True)


#Connect to MovieRecommender database on local server
conn = mysql.connector.connect(user='root',
                               password='vhyirj981022',
                               host='localhost',
                               database='MovieRecommender')
cursor = conn.cursor()

#Create needed tables
cursor.execute("CREATE TABLE Movie(MovieId INT AUTO_INCREMENT PRIMARY KEY, Title VARCHAR(128), Year INT(4), Description VARCHAR(255))")
cursor.execute("CREATE TABLE Ratings(RatingId INT AUTO_INCREMENT PRIMARY KEY, MovieId INT, Rating INT, FOREIGN KEY (MovieId) REFERENCES Movie(MovieId))")
cursor.execute("CREATE TABLE Director(DirectorId INT AUTO_INCREMENT PRIMARY KEY,FirstName VARCHAR(50),LastName VARCHAR(50))")
cursor.execute("CREATE TABLE GenreToMovie(MovieId INT, Genre VARCHAR(50), FOREIGN KEY (MovieId) REFERENCES Movie(MovieId))")
cursor.execute("CREATE TABLE DirectorToMovie(DirectorId INT,MovieId INT, FOREIGN KEY (MovieId) REFERENCES Movie(MovieId),FOREIGN KEY (DirectorId) REFERENCES Director(DirectorId))")

#Create table with ratings for each movie
cursor.execute("CREATE VIEW averageRatings(movieId, rating) as SELECT movieId,avg(rating) FROM Ratings GROUP BY MovieId")

#Iterate over dataframes --> cast numbers to strings as needed
for index,row in Director.iterrows():
    cursor.execute('INSERT INTO Director (FirstName, LastName) VALUES ("'+row["FirstName"]+'","'+row["LastName"]+'")')

for index,row in Movie.iterrows():
    cursor.execute('INSERT INTO Movie (Title, Year,Description) VALUES ("'+row["Title"]+'",'+str(row["Year"])+',"'+row["Description"]+'")')

for index,row in Rating.iterrows():
    cursor.execute('INSERT INTO Ratings (MovieId,Rating) VALUES("'+str(row["MovieId"]) +'","' + str(row["Rating"]) +'")')

for index,row in GenreToMovie.iterrows():
    cursor.execute('INSERT INTO GenreToMovie (MovieId,Genre) VALUES ("'+str(row["MovieId"])+'","'+row["Genre"]+'")')

for index,row in DirectorToMovie.iterrows():
    cursor.execute('INSERT INTO DirectorToMovie (DirectorId,MovieId) VALUES ("'+str(row["DirectorId"])+'","'+str(row["MovieId"])+'")')

cursor.execute("SELECT count(*) FROM Movie")
movies = cursor.fetchall()
print(movies)
cursor.execute("SELECT MovieId,Rating FROM averageRatings")
movies = cursor.fetchall()
print(movies)
conn.commit()
conn.close()

