from datetime import datetime
TICKET_FORMAT = '''
-------------------------------------
ID: {id}
CREATED AT: {created_at}
SUBJECT: {subject}
DESC: {desc}
-------------------------------------
'''


#Given list of json tickets, writes to file
#in readable way, terminating once tickets are past
#end time
def output_tickets(tickets, out_file, end_time):
    #Tickets are dictionaries/json formatted
    for ticket in tickets:
        if date_to_epoch(ticket['created_at']) >= end_time:
            break
        else:
            out_file.write(beautify_ticket(ticket))
    return

#Given json ticket, returns readable
#multiline ticket string
def beautify_ticket(ticket):
    return TICKET_FORMAT.format(id=ticket['id'], created_at=ticket['created_at'],
                                subject=ticket['subject'], desc=ticket['description'])

def date_to_epoch(date):
    e = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    return e.timestamp()