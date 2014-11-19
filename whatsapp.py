from datetime import datetime
import codecs
import json

file = open('data/WhatsApp_Mela.txt')

out_events = []
message = {}

def convert_to_timestamp(time):
        return int((time - datetime.fromtimestamp(0)).total_seconds())

for line in file:
    if line.startswith(codecs.BOM_UTF8):
        line = line[3:]
    if line.count(':') > 2 and (line.find('Kris') > 0 or line.find('Mela') > 0):
        if message:
            out_events.append(message)
            message = {}
        nameindex = line.index('M')+1
        timestr = line[:nameindex].strip()
        time = datetime.strptime(timestr + ' EST', '%m/%d/%y, %I:%M:%S %p %Z')
        msgindex = line.index(':', nameindex+1)
        name = line[nameindex+2:msgindex]
        msg = line[msgindex+2:].strip()
        message = {'name' : name.split(' ')[0], 'ts' : convert_to_timestamp(time), 'message': msg}
    else:
        message['message'] +=  " " + line.strip()

out_events.append(message)

sorted_out = sorted(out_events, key= lambda k: float(k[u'ts']))
out_file = open('data/whatsapp.json', 'w')
json.dump(sorted_out, out_file, indent=0)
out_file.close()