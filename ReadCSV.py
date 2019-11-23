import pandas

Director = pandas.read_csv('Director.csv')
DirectorToMovie = pandas.read_csv('DirectorToMovie.csv')
Movie = pandas.read_csv('Movie.csv')
GenreToMovie = pandas.read_csv('GenreToMovie.csv')

print(Director)
print(DirectorToMovie)
print(Movie)
print(GenreToMovie)

for i,j in Director.iterrows():
    print(j["FirstName"])
    print(j["LastName"])



