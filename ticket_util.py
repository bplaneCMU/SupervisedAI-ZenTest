#Given list of json tickets, writes to file
#in readable way, terminating once tickets are past
#end time
def output_tickets(tickets, out_file, end_time):
    #Tickets are dictionaries/json formatted
    for ticket in tickets:
        
    return

#Given json ticket, returns readable
#multiline ticket string
def beautify_ticket(ticket):
    return TICKET_FORMAT.format(id=ticket['id'], created_at=ticket['created_at'],
                                subject=ticket['title'], desc=ticket['description'])

def date_to_timestamp(date):
    e = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    return