from sys import argv
from ticket_util import *
import requests as http
import json
import time as t
from math import floor

def __main(email, subdomain, token):
    #Format email and token for BasicAuthentication
    email = email + '/token'
    auth_tuple = (email, token)

    out_file = open('tickets' + str(floor(t.time())) + '.txt', 'w')

    time = START_TIME
    x_rate = 700 #Requests remaining in this minute
    end_of_stream = False
    while time < END_TIME and not end_of_stream:
        #Format and make request
        request = REQUEST.format(sub_domain=subdomain, unix_time=time)
        r = http.get(request, headers=HEADERS, auth=auth_tuple)

        #Convert responce text to a dictionary
        responce = json.loads(r.text)

        #Handle Error codes
        if(r.status_code >= 400):
            print(str(r.status_code), 'Request Error:', responce['error'])
            break
        
        #Parse responce json/dictionary
        #Don't just crash on malformed responce
        try:
            end_of_stream = responce['end_of_stream']
            time = responce['end_time']
            tickets = responce['tickets']
        except:
            print('Malformed responce\n', r.text)
            break

        output_tickets(tickets, out_file, END_TIME)


        #If total requests exceeds 700 (the Zendesk 'team' plan)
        #Assume this process was much less than a min -> sleep for a min
        x_rate += -1
        if(x_rate <= 0):
            print('Requests per minute exceeded\n Processing will resume in one minute')
            t.sleep(60)
            x_rate = 700
    return

#If main file being executed from command line
if __name__ == '__main__':
    #Define script specific globals
    HEADERS = {'Content-Type' : 'application/json',
               'Accept' : 'application/json'}
    START_TIME = 1576411200
    END_TIME = 1578657600
    REQUEST = 'https://{sub_domain}.zendesk.com/api/v2/incremental/tickets.json?start_time={unix_time}'


    #Parse arguments
    #Expecting:
    #Email
    #Subdomain
    #Authentication token
    if len(argv) == 4 and '@' in argv[1]:
        __main(argv[1], argv[2], argv[3])
    else:
        print('Usage:', 
              'python3 zenrequest.py [email@domain.com] [zendesk subdomain] [API authtoken]')
