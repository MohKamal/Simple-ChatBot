import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from keras.models import load_model
model = load_model('chatbot_model\chatbot_model.h5')
import json
import random
import cgi
import cgitb
from datetime import datetime

intents = json.loads(open('chatbot_model\intents.json').read())
words = pickle.load(open('chatbot_model\words.pkl','rb'))
classes = pickle.load(open('chatbot_model\classes.pkl','rb'))
cgitb.enable()

def clean_up_sentence(sentence):
    # tokenize the pattern - splitting words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stemming every word - reducing to base form
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


# return bag of words array: 0 or 1 for words that exist in sentence
def bag_of_words(sentence, words, show_details=True):
    # tokenizing patterns
    sentence_words = clean_up_sentence(sentence)
    # bag of words - vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,word in enumerate(words):
            if word == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % word)
    return(np.array(bag))

def predict_class(sentence):
    # filter below  threshold predictions
    p = bag_of_words(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sorting strength probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def print_header():
    print ("""Content-type: text/html\n
    <!DOCTYPE html>
    <html>
    <body>""")

def print_close():
    print ("""</body>
    </html>""")

def display_data(param1):
    ints = predict_class(param1)
    res = getResponse(ints, intents)
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    print("Current Time =", current_time)
    print_header()
    print('<p>' + res + '</p>')
    print('<span>' + current_time + '</span>')
    print_close()

def display_error():
    print_header()
    print ("<p>Ooops! Sorry, error here!</p>")
    print_close()

def main():
    form = cgi.FieldStorage()
    if ("human_message" in form):
        display_data(form["human_message"].value)
    else:
        display_error()

main()