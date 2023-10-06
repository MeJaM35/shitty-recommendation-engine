import sqlite3
import numpy as np

con = None

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
    query = 'SELECT post_id from core_post'
    cursor = con.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def fetch_posts():
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

def fetch_interactionscores(userid):
    query = 'SELECT pt.tagid, SUM(pt.score) AS total_score FROM User_Interactions ui JOIN Post_tags pt ON ui.postid = pt.postid WHERE ui.userid ="'+userid+'"GROUP BY pt.tagid;'
    cursor = con.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def normalise(interactions):
    largest_score = max(interactions.values())
    reduction_factor = largest_score/10
    for tag in interactions:
        interactions[tag] /= reduction_factor
    return interactions

def generatescores(interests, interactions):
    average_scores = {}
    # Iterate through user_interests and user_interactions to calculate the average
    for tag in user_interests:
        if tag in user_interactions:
            # Calculate the average by summing the scores and dividing by 2
            average_score = (user_interests[tag] + user_interactions[tag]) / 2
            average_scores[tag] = average_score
        else:
            # If the tag is not present in user_interactions, use the user_interests score
            average_scores[tag] = user_interests[tag]   
    return average_scores

def updatescore(scores, userid):
    cursor = con.cursor()
    for tag, score in scores.items():
        query = 'UPDATE core_userinterests SET score = "'+score+'" WHERE userid = "'+userid+'" AND tagid = "'+tag+'";'
        cursor.execute(query)
    con.commit()

def cosine_similarity(dict1, dict2):
    # Extract unique keys from both dictionaries
    all_keys = set(dict1.keys()).union(dict2.keys())
    # Create vectors for each dictionary based on the keys
    vector1 = [dict1.get(key, 0) for key in all_keys]
    vector2 = [dict2.get(key, 0) for key in all_keys]
    # Calculate the cosine similarity using the modified vectors
    dot_product = np.dot(vector1, vector2)
    magnitude1 = np.linalg.norm(vector1)
    magnitude2 = np.linalg.norm(vector2)
    similarity = dot_product / (magnitude1 * magnitude2)
    return similarity

def recommend(userid, postid):
    query = 'INSERT into core_recommendations (post_id, user_id) values ('+postid+','+userid+')'
    cursor = con.cursor()
    cursor.execute(query)
    con.commit()

#def cacheinteractions()
#def insertempty(userid)

con = connect_db('C:/Users/varad/Desktop/django-freelance/giggity/db.sqlite3')
users = fetch_users()
posts = fetch_posts()
# Iterate over users
for r in users:
    user = r[0]
    # Fetching user interests
    user_interests = {}
    for row in fetch_userinterests(user):
        tag = row[0]
        score = row[1]
        user_interests[tag] = score
    # Start collecting user interactions
    user_interactions = {}
    for row in fetch_interactionscores(user):
        tag = row[0]
        score = row[1]
        user_interactions[tag] = score
    # Normalise interaction scores to 10
    user_interactions = normalise(user_interactions)
    user_scores = generatescores(user_interests, user_interactions)
    updatescore(user_scores, user)
# Iterate over posts
for r in posts:
    post = r[0]
    # Fetch post tags
    post_tags = {}
    for row in fetch_posttags(post):
        tag = row[0]
        score = row[1]
        post_tags[tag] = score
    # Iterate over users
    for row in users:
        user = row[0]
        user_interests = {}
        for row in fetch_userinterests(user):
            tag = row[0]
            score = row[1]
            user_interests[tag] = score 
        similarity = cosine_similarity(user_interests, post_tags)
        if similarity > 0.5:
            recommend(user, post, similarity)
