from HTMLParser import HTMLParser
from datetime import datetime
from datetime import timedelta
import json
import os

class GTalkParser(HTMLParser):
    message = None
    currentUser = None
    state = 0
    datestr = ''
    starttime = None

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name != 'class':
                continue
            if value == 'aO1':
                self.state = 'user'
            elif value == 'aOT':
                self.state = 'message'
            elif value == 'aSy':
                self.state = 'time'
            elif value == 'aOM':
                self.state = 'startdate'
            elif value == 'aZc':
                self.state = 'starttime'
            else:
                self.state = ''

    def handle_data(self, data):
        data = data.strip()
        if len(data) == 0:
            return

        if self.state == 'user':
            if data == 'Brangi Brangelina': self.currentUser = u'Mela'
            elif data == 'Kris Jurgowski':  self.currentUser = u'Kris'
            else: print data

        elif self.state == 'message':
            if not self.message:
                self.message = {'name': self.currentUser, 'message': data}
            else:
                self.message['message'] += " " + data

        elif self.state == 'time':
            self.update_with_time(data)
            if not self.message:
                return
            self.message['ts'] = self.convert_to_timestamp(self.starttime)
            out_event = self.message
            out_events.append(out_event)
            self.message = None

        elif self.state == 'startdate':
            self.datestr = data + " "

        elif self.state == 'starttime':
            timestr = self.datestr + data + ' EST'
            self.starttime = datetime.strptime(timestr, '%A, %B %d, %Y %I:%M %p %Z')

        # else:
        #     print data

    def convert_to_timestamp(self, time):
        return int((time - datetime.fromtimestamp(0)).total_seconds())

    def update_with_time(self, timestr):
        parts = timestr.split(':')
        hour = int(parts[0])
        parts = parts[1].split(' ')
        midday = parts[1]
        if hour == 12:
            hour = 0 if midday == 'AM' else 12
        elif midday == 'PM':
            hour += 12
        min = int(parts[0])
        newtime = self.starttime.replace(hour=hour, minute=min)
        if (newtime == self.starttime):
            newtime = newtime + timedelta(seconds=1)
        else:
            newtime = newtime.replace(second=0)
        if newtime < self.starttime:
            newtime += timedelta(days=1)
        self.starttime = newtime



out_events = []
parser = GTalkParser()

#file = open('data/Hangouts/2014-05-09.html')



for name in os.listdir('data/Hangouts'):
    file = open('data/Hangouts/' + name)
    parser.feed(file.read().replace("<wbr>", ""))

sorted_out = sorted(out_events, key= lambda k: float(k[u'ts']))
out_file = open('data/brangi_old.json', 'w')
json.dump(sorted_out, out_file, indent=0)
out_file.close()