# Getting Data from SQLite database and rearrange it to the json file that the model can read it

import sqlite3
import json
from datetime import datetime

timeframe = '2015-01'

connection = sqlite3.connect('oumayma\{}.db'.format(timeframe))
c = connection.cursor()

# Find the parent comment for a special comment
def find_parent(pid):
    try:
        sql = "SELECT comment FROM parent_reply WHERE comment_id = '{}' LIMIT 1".format(pid)
        c.execute(sql)
        result = c.fetchone()
        if result != None:
            return result[0]
        else: return False
    except Exception as e:
        print("Line 20 = " + str(e))
        return False

# Getting data from database to dictiony and then saving it ot json file
def getArray():
    intentsGlobal = {} # Global Dictionary to save to file
    tags = [] # All tages, child of intentsGlobal
    rowCount = 0
    totlaRowCount = 0
    tagsCount = 0 
    totalTagsCount = 0
    try:
        sql = "SELECT DISTINCT subreddit FROM parent_reply" # Select subreddit to make them tags
        c.execute(sql)
        subreddits = c.fetchall()
        print("Total Tags : {}".format(len(subreddits)))
        totalTagsCount = len(subreddits)
        # Foreach subreddits and getting all comments related to them
        for sub in subreddits:
            sql = "SELECT * FROM parent_reply WHERE subreddit = '{}' ".format(sub[0])
            c.execute(sql)
            rows = c.fetchall()
            tag = {}
            tag["tag"] = sub[0]
            questions = []
            responses = []
            # Foreach the rows that follow a tag (subreddit)
            # If parent comment exist, it will be the question and current comment is the response
            # If not, current comment is a question without response
            for row in rows:
                parent = find_parent(row[0])
                if parent != False :
                        questions.append(parent)
                        responses.append(row[3])
                else:
                    questions.append(row[3])
                rowCount += 1
            totlaRowCount += rowCount
            print("Tag: {} - Rows added: {} - Total Rows: {}".format(sub[0], rowCount, totlaRowCount))
            rowCount = 0
            # After the loop is finished for a subreddit
            # Adding the tag and questions and responses to the Tags arrray
            tag["patterns"] = questions
            tag["responses"] = responses
            tag["context"] = ""
            tags.append(tag)
            tagsCount += 1
            print("Total Tags: {} - Tags added: {} - Tags left: {}".format(totalTagsCount, tagsCount, (totalTagsCount - tagsCount)))
                
                

    except Exception as e:
        print("Line 61 = " + str(e))
    # After the loops, we gonna put the Tags array inside the intentsGlobal dictionary and save it to json file
    intentsGlobal["intents"] = tags
    with open('intents_test.json', 'w') as f:
        json.dump(intentsGlobal, f)

    
if __name__ == '__main__':
    getArray()