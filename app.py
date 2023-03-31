from helper import helper
from db_operations import db_operations

#create connection path to playlist database, create clean data from songs.csv
db_ops = db_operations("playlist.db")
data = helper.data_cleaner("songs.csv")

#start screen of code
def startScreen():
    print("Welcome to your playlist!")

#returns if songs table has any records
def is_empty():
    query = '''
    SELECT COUNT(*)
    FROM songs;
    '''

    result = db_ops.single_record(query)
    return result == 0

#fills table from songs.csv if it's empty
def pre_process():
    if is_empty():
        attribute_count = len(data[0])
        placeholders = ("?,"*attribute_count)[:-1]
        query = "INSERT INTO songs VALUES("+placeholders+")"
        db_ops.bulk_insert(query, data)

    answer = input("Do you want to load new songs into the database (y/n)?\n")
    if answer == "y":
        try:
            filename = input("What is the name of your file? ")
            data = helper.data_cleaner(filename)
            attribute_count = len(data[0])
            placeholders = ("?,"*attribute_count)[:-1]
            query = "INSERT INTO songs VALUES("+placeholders+")"
            db_ops.bulk_insert(query,data)
        except:
            print("Could not import file.")
        
#show user menu options
def options():
    print('''Select from the following menu options: 
    1. Find songs by artist
    2. Find songs by genre
    3. Find songs by feature
    4. Update song by name
    5. Delete song by name
    6. Exit''')
    return helper.get_choice([1,2,3,4,5,6])

#search the songs table by artist
def search_by_artist():
    #get list of all artists in table
    query = '''
    SELECT DISTINCT Artist
    FROM songs;
    '''
    print("Artists in playlist: ")
    artists = db_ops.single_attribute(query)

    #show all artists, create dictionary of options, and let user choose
    choices = {}
    for i in range(len(artists)):
        print(i, artists[i])
        choices[i] = artists[i]
    index = helper.get_choice(choices.keys())

    #user can ask to see 1, 5, or all songs
    print("How many songs do you want returned for", choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1,5,0])

    #print results
    query = '''SELECT DISTINCT name
    FROM songs
    WHERE Artist =:artist ORDER BY RANDOM()
    '''
    dictionary = {"artist":choices[index]}
    if num != 0:
        query +="LIMIT:lim"
        dictionary["lim"] = num
    results = db_ops.name_placeholder_query(query, dictionary)
    helper.pretty_print(results)

#search songs by genre
def search_by_genre():
    #get list of genres
    query = '''
    SELECT DISTINCT Genre
    FROM songs;
    '''
    print("Genres in playlist:")
    genres = db_ops.single_attribute(query)

    #show genres in table and create dictionary
    choices = {}
    for i in range(len(genres)):
        print(i, genres[i])
        choices[i] = genres[i]
    index = helper.get_choice(choices.keys())

    #user can ask to see 1, 5, or all songs
    print("How many songs do you want returned for", choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1,5,0])

    #print results
    query = '''SELECT DISTINCT name
    FROM songs
    WHERE Genre =:genre ORDER BY RANDOM()
    '''
    dictionary = {"genre":choices[index]}
    if num != 0:
        query +="LIMIT:lim"
        dictionary["lim"] = num
    results = db_ops.name_placeholder_query(query, dictionary)
    helper.pretty_print(results)

#search songs table by features
def search_by_feature():
    #features we want to search by
    features = ['Danceability', 'Liveness', 'Loudness']
    choices = {}

    #show features in table and create dictionary
    choices = {}
    for i in range(len(features)):
        print(i, features[i])
        choices[i] = features[i]
    index = helper.get_choice(choices.keys())

    #user can ask to see 1, 5, or all songs
    print("How many songs do you want returned for", choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1,5,0])

    #what order does the user want this returned in?
    print("Do you want results sorted in asc or desc order?")
    order = input("ASC or DESC: ")

    #print results
    query = "SELECT DISTINCT name FROM songs ORDER BY "+choices[index]+" "+order
    dictionary = {}
    if num != 0:
        query +=" LIMIT:lim"
        dictionary["lim"] = num
    results = db_ops.name_placeholder_query(query, dictionary)
    helper.pretty_print(results)

# Update songs by name
def song_update():
    songName = input("What song do you want to update?\n")

    query = 'SELECT * FROM songs WHERE Name = \''+songName+'\''
    song_results = db_ops.print_row(query)

    try:
        id = str(song_results[0][0])
    except:
        print("Song not found!\n")
        return

    print('''What do you want to modify?\n
    1) Song Name 
    2) Album Name
    3) Artist Name 
    4) Release Date
    5) Explicit 
    '''
    )
    print(song_results)

    choice = helper.get_choice([1,2,3,4,5])
    try:
        match choice:
            case 1:
                newInfo = input("What new song name do you want?\n")
                query = 'UPDATE songs SET Name = \''+newInfo+'\'  WHERE songID = \''+id+'\''
                db_ops.update(query)
            case 2: 
                newInfo = input("What new album name do you want?\n")
                query = 'UPDATE songs SET Album = \''+newInfo+'\'  WHERE songID = \''+id+'\''
                db_ops.update(query)
            case 3: 
                newInfo = input("What new artist do you want?\n")
                query = 'UPDATE songs SET Artist = \''+newInfo+'\'  WHERE songID = \''+id+'\''
                db_ops.update(query)
            case 4: 
                newInfo = input("What new date do you want?\n")
                query = 'UPDATE songs SET releaseDate = \''+newInfo+'\'  WHERE songID = \''+id+'\''
                db_ops.update(query)
            case 5: 
                newInfo = input("What new explicit info do you want?\n")
                query = 'UPDATE songs SET Explicit = \''+newInfo+'\'  WHERE songID = \''+id+'\''
                db_ops.update(query)
    except:
        print("Wrong syntax! Try again\n")

# Delete Song by Name
def delete_song():
    songName = input("What song do you want to delete?\n")
    #get the song info
    try:
        query = 'SELECT * FROM songs WHERE Name = \''+songName+'\''
        song_results = db_ops.single_record(query)
        #get the id 
        id = str(song_results)
        print("Deleted song id: ", id)
        #run a query
        query = 'DELETE FROM songs WHERE Name = \''+songName+'\''
        db_ops.update(query)
    except:
        print("Song not found!\n")

#main program
startScreen()
pre_process()

#main program loop
while True:
    user_choice = options()
    if user_choice == 1:
        search_by_artist()
    if user_choice == 2:
        search_by_genre()
    if user_choice == 3:
        search_by_feature()
    if user_choice == 4:
        song_update()
    if user_choice == 5:
        delete_song()
    if user_choice == 6:
        print("Goodbye!")
        break

db_ops.destructor()