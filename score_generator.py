def connect_db(db_name):
    # Tries to connect 50 times after that stops script execution
    for x in range(50)
        try:
            connection = sqlite3.connect(db_name)
            # Connection success! Break out of for loop as well as function and return connection to main
            return connection
        except sqlite3.Error as e:
            # Display error and attempt number in console
            print(" Failed to connect, retrying times:"+x+" Error:"+e)
    # Could not connect 50 times so stop execution of the script
    sys.exit(1)

def fetch_users():
    query = 'SELECT id from core_userprofile'
    cursor = con.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def fetch_interactions(userid):
    query = 'SELECT postid from core_interaction WHERE userid="'+userid+'";'
    cursor = con.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    return results
    
def fetch_userinterests(userid):
    query = 'SELECT tagid, score from core_userinterests WHERE userid="'+userid+'";'
    cursor = con.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def fetch_posttags(postid):
    query = 'SELECT tagid from core_post_tags WHERE post_id="'+postid+'";'
    cursor = con.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    return results

#def generatescores(interests, interactions)
#def cacheinteractions()
#def insertempty(userid)

con = connect_db('C:/Users/varad/Desktop/django-freelance/giggity/db.sqlite3')
users = fetch_users()
for r in users:
    user = r[0]
    user_interests = {}
    for row in fetch_userinterests(user):
        tag = row[0]
        score = row[1]
        user_interests[tag] = score
    user_interactions = {}
    for row in fetch_interactions(user):
        postid = row[0]
        for record in fetch_posttags(postid):
