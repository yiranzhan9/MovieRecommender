import mysql.connector
import http.server
import socketserver
import urllib.parse
from io import BytesIO
#https://dev.mysql.com/doc/refman/8.0/en/osx-installation-pkg.html
#https://dev.mysql.com/doc/refman/8.0/en/osx-installation-launchd.html
#ThisIsASecurePassword1313

#Open connection to DataBase
conn = mysql.connector.connect(user='root',
                               password='ThisIsASecurePassword1313',
                               host='localhost',
                               database='MovieRecommender')
cursor = conn.cursor()

#Set port for server access at localhost:PORT
PORT = 8080

#Find and open needed files
#TODO JQuery Autocomplete to replace select https://jqueryui.com/autocomplete/
RateMovie = open("html/RateMovie.html","rb").read()

#Break of Rate/Recommend to insert options into when page is requested
#Can replaces with cached results instead of calling for each request
rateStart = """<!DOCTYPE html>
<html>
    <head>
        <title>Rate Movie</title>
        <link rel="stylesheet" type="text/css" href="/css/style.css">
    </head>
    <h1>Rate a Movie</h1>
    <div>
        <form method="post">
            <div>
                <label for="movieTitle">Movie: </label>
                <select name="movieTitle" required>"""
rateEnd = """</select>
            </div>
            <div>
                <label for="rating">Rating: </label>
                <select name="rating" required>
                    <option> 1 </option>
                    <option> 2 </option>
                    <option> 3 </option>
                    <option> 4 </option>
                    <option> 5 </option>
                    <option> 6 </option>
                    <option> 7 </option>
                    <option> 8 </option>
                    <option> 9 </option>
                    <option> 10 </option>
                </select>
            </div>
            <div>
                <input type="submit">
            </div>
        </form>
    </div>
</html> """

recommendStart = '<!DOCTYPE html><html><head><title>Get Recommendation </title><link rel="stylesheet" type="text/css" href="css/style.css"></head>'
recommendStart += '<h1>Choose a Genre</h1><div><form method="post"><div><label for="genre">Rating: </label><select name="genre" required>'
recommendEnd = '</select></div><div><input type="submit"></div></form></div></html>'

css = open("css/style.css","rb").read()

#Gets genre recommendation from db
#TODO: Add error handling of no rated movies of a genre
def getReccomendation(genre):
    cursor.execute("SELECT MovieId,Title,Year,Description,Rating FROM Movie INNER JOIN GenreToMovie using(MovieId) INNER JOIN averageRatings using(MovieId) WHERE Genre = " + genre + "GROUP BY MovieId ORDER BY Rating DESC LIMIT 3" )
    movies = cursor.fetchall()
    htmlTable = '<table><tr><th style="text-align:left">Title</th><th>Year</th><th>Directors</th><th>Rating</th><th>Description</th></tr>'
    for movie in movies:
        htmlTable += '<tr><td>'+movie[1]+'</td>'
        htmlTable += '<td>'+str(movie[2])+'</td>'
        cursor.execute("SELECT FirstName,LastName From DirectorToMovie INNER JOIN Director using(DirectorId) WHERE MovieId =" + str(movie[0]))
        directors = cursor.fetchall()
        htmlTable += '<td><ul>'
        for director in directors:
            htmlTable += '<li>' + director[0] + '&nbsp;' + director[1] + '</li>'
        htmlTable += '</ul></td><td>'+str(movie[4])+'</td>'
        htmlTable += '<td>'+movie[3]+'</td></tr>'
    return htmlTable + '</table>'
    
#Adds rating to database
def submitRating(movieId,rating):
    #convert from bytes to string to int
    movieId = int(str(movieId, 'utf-8'))
    rating = int(str(rating, 'utf-8'))
    cursor.execute('INSERT INTO Ratings (MovieId,Rating) VALUES("'+str(movieId) +'","' + str(rating) +'")')
    conn.commit()
    
#Get list of all titles for select on rating
def getTitles():
    cursor.execute("SELECT Title,Year,MovieId FROM Movie")
    movies = cursor.fetchall()
    movies.sort()
    print(movies)
    movieList = ""
    for movie in movies:
        movieList += '<option value="'+str(movie[2])+'">'+movie[0]+ " (" + str(movie[1])+")</option>"
    return movieList

#Get list of genres for recommendation
def getGenres():
    cursor.execute("SELECT DISTINCT genre FROM GenreToMovie")
    genres = cursor.fetchall()
    genres.sort()
    print(genres)
    genreList = ""
    for genre in genres:
        genreList += "<option>"+genre[0]+"</option>"
    return genreList

#Handles http request (get,post)
#ToDo --> dynamically get genres list JS?
#ToDo --> dynamically get movie list JS?
#make sorted lists
class Handler(http.server.BaseHTTPRequestHandler):
    #Sends requested Html,CSS file or send links to proper html pages
    def do_GET(self):
        print(self.path)
        self.send_response(200)
        self.end_headers()
        if self.path == "/RateMovie.html":
            print("rate")
            self.wfile.write(str.encode(rateStart +getTitles()+ rateEnd))
        elif self.path == "/RecommendMovie.html":
            print("recommend")
            self.wfile.write(str.encode(recommendStart +getGenres()+ recommendEnd))

        elif self.path == "/css/style.css":
            print("css")
            self.wfile.write(css)
        else:
            print("other")
            self.wfile.write(b'<!DOCTYPE html><html><head><link rel="stylesheet" type="text/css" href="css/style.css"></head><div><a href="/RateMovie.html">RateMovie</a><br><a href="/RecommendMovie.html">RecMovie</a></div></html>')

    #Parse request for paramerters else return error
    #ToDo change to return error code if invalid request 403?
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        field_data = self.rfile.read(length)
        fields = urllib.parse.parse_qs(field_data)
        body = b"Parameters:\n"
        #Get parameters of post form
        for k in fields:
            body += b"" + k + b": " + fields[k][0] + b"\n"

        # contains movieTitle, rating --> rating form
        if b"movieTitle" in fields and b"rating" in fields:
            submitRating(fields[b"movieTitle"][0],fields[b"rating"][0] )
            body = b'Rating Submitted'

        # contains genre --> recommendation form
        elif b"genre" in fields:
            body = '<!DOCTYPE html><html><head><link rel="stylesheet" type="text/css" href="css/style.css"></head><div>'
            body += '<h1>Top Rated ' + str(fields[b"genre"][0])[2:-1] + ' Movies</h1>'
            body += getReccomendation(str(fields[b"genre"][0])[1:])
            body += '</div></html>'
            body = str.encode(body)
        # neither --> error
        else:
            body += b"invalid params"
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(body)
        self.wfile.write(response.getvalue())

# Start server at given port        
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        conn.close();

    
