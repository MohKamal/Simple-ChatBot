import json

intents_file = open('intents_db.json').read()
intents = json.loads(intents_file)
intentCount = 0
small_intents = []
intentsGlobal = {}


for intent in intents['intents']:
    print("Current Tag: {}".format(intent['tag']))
    small_intents.append(intent)
    intentCount += 1
    if intentCount == 3:
        break

intentsGlobal["intents"] = small_intents
with open('intents_small.json', 'w') as f:
    json.dump(intentsGlobal, f)