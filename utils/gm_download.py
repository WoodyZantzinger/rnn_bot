__author__ = 'woodyzantzinger'

import requests
import sys
import json
import random
import pdb
from progressbar import ProgressBar

#USE: Determine if a A -> B message pair is a valid match for pairing
def validate(a_message, b_message):
    try:
        #check nulls
        if a_message == None or b_message == None: return False
        if a_message == "" or b_message == "": return False

        #check timing. We only want messages within 100 seconds of each other? Time incremenets so it is B - A
        if ( int(b_message["created_at"]) - int(a_message["created_at"]) ) > 100: return False

        #check user to make sure sUN not involved. We only want real people
        if a_message["sender_id"] == "" or b_message["sender_id"] == "": return False
        if a_message["sender_id"] == "219313" or b_message["sender_id"] == "219313": return False

        #check URL / Images / Odd stuff
        if a_message["text"].find("http") > 0 or b_message["text"].find("http") > 0: return False #Basic ass URL check?
        if a_message["text"].find("#oracle") > 0 or b_message["text"].find("#oracle") > 0: return False #No Oracle
        if a_message["text"].find("#debugoracle") > 0 or b_message["text"].find("#debugoracle") > 0: return False #No Oracle


    #If anything here fails, these are unusual messages
    except KeyError:
        return False

    #A and B passed every check!
    return True



#STATIC
request_url = "https://api.groupme.com/v3/groups/13203822/messages?token=xde396cxXkwCQjn2BZQiVojW9XLYd4NxIiYepwwx&limit=100"
valid_pairs = []

response = requests.get(request_url)

#Get number of messages and most recent message ID
counted_messages = 0
total_messages = int(response.json()["response"]["count"])
after_id = int(response.json()["response"]["messages"][0]["id"])

print "Fetching %d Messages starting with ID = %d\n" % (total_messages, after_id)

pbar = ProgressBar(
    maxval=total_messages,
)

#start with Empty A, B
A = None
B = None

pbar.start()
while(counted_messages < total_messages):

    #Fetch Messages
    response = requests.get(request_url + "&before_id=" + str(after_id))
    messages = response.json()["response"]["messages"]

    #loop through every message to find A-> B pair
    #We reverse so it begins with oldest message
    old_message = []
    for message in reversed(messages):

        if A != None and B == None:
            #We have a start, need an end!
            if validate(A, message):
                B = message
            else:
                #We weren't able to validate the A-B pair, so remove both and lets start over
                A = None
                B = None

        if A == None:
            #We need a start!
            A = message

        if A != None and B != None:
            #We found a valid pair!
            valid_pairs.append([A, B])
            #remove and start over!
            A = None
            B = None

        #push the current message onto the stack
        old_message = message


    #Increment counted
    pdb.set_trace()
    counted_messages += len(messages)

print "Found %d Valid Pair" % len(valid_pairs)

for x in range(0, 50):
    r = random.randint(1,len(valid_pairs))
    print "( %s ) -> ( %s )" % (valid_pairs[r][0]["text"], valid_pairs[r][1]["text"])