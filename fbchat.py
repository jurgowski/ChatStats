from HTMLParser import HTMLParser
from datetime import datetime
import json


class FBParser(HTMLParser):
    message = None
    currentUser = None
    state = ''
    threads = 0

    def handle_starttag(self, tag, attrs):
        if self.threads > 1:
            return

        if tag == 'p':
            self.state = 'message'
            return

        for name, value in attrs:
            if name != 'class':
                continue
            if value == 'user':
                self.state = 'user'
            elif value == 'meta':
                self.state = 'time'
            elif value == 'thread':
                    self.commit()
                    self.threads += 1

    def handle_data(self, data):
        if self.threads > 1:
            return

        if self.state == 'user':
            self.commit()
            if data == 'Meli Olczy': self.currentUser = u'Mela'
            elif data == 'Kris Jurgowski':  self.currentUser = u'Kris'
            else: print data

        elif self.state == 'message':
            if not self.message.get('message'):
                self.message['message'] = data
            else:
                self.message['message'] += " " + data
            # out_event = self.message
            # out_events.append(out_event)

        elif self.state == 'time':
            time = datetime.strptime(data, '%A, %B %d, %Y at %I:%M%p %Z')
            self.message = {'name': self.currentUser, 'ts':self.convert_to_timestamp(time)}

        elif self.state == 'end':
            out_events.append(self.message)
            self.reset()

        else:
            print data

    def convert_to_timestamp(self, time):
        return int((time - datetime.fromtimestamp(0)).total_seconds())

    def commit(self):
        if self.message:
            print self.message
            out_events.append(self.message)
            self.message = None

out_events = []

html_data = open('data/messages.htm')

parser = FBParser()
parser.feed(html_data.read())


sorted_out = sorted(out_events, key= lambda k: float(k[u'ts']))
out_file = open('data/meli_fb.json', 'w')
json.dump(sorted_out, out_file, indent=0)
out_file.close()