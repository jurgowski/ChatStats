import json
import datetime
from pprint import pprint

def fetchUsers(participants):
    user_map = {}

    for participant in participants:
        chat_id = participant['id']['chat_id']
        name = participant.get('fallback_name','?')
        user_map[chat_id] = name

    return user_map

json_data = open('data/Hangouts.json')

data = json.load(json_data)

conversation_states = data['conversation_state']
#pprint(conversation_states[40])


# for state in conversation_states:
#     conversation_state = state['conversation_state']
#     participants = conversation_state['conversation']['participant_data']
#     fetchUsers(participants)

conversation_state = conversation_states[8]['conversation_state']
user_map = {u'116957312546171844361': u'Kris', u'104948165872551677495': u'Mela'}
events = conversation_state['event']

out_events = []

for event in events:
    chat = event.get('chat_message')
    if not chat:
        continue

    message_parts = []
    message_content = event['chat_message']['message_content']

    if not message_content.get('segment'):
        continue

    for segment in message_content['segment']:
        if segment['type'] in ('TEXT', 'LINK'):
            message_parts.append(segment['text'])

    name = user_map[event['sender_id']['chat_id']]
    message = " ".join(message_parts)
    date = int(float(event['timestamp'])/1000000)
    # print u'{2} {0}: {1}'.format(name, message, date)
    out_event = {u'ts' : date, u'name' : name, u'message' : message}
    out_events.append(out_event)

json_data.close()

sorted_out = sorted(out_events, key= lambda k: float(k[u'ts']))

out_file = open('data/brangi.json', 'w')
json.dump(sorted_out, out_file, indent=0)
out_file.close()






