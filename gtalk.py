from HTMLParser import HTMLParser

class GTalkParser(HTMLParser):
    message = None
    currentUser = None
    state = 0

    def handle_starttag(self, tag, attrs):
        print attrs

        classtag = attrs.filter(lambda x:x[0] == 'class')
        print classtag
        return 
        if atclass == 'a01':
            self.state = 1
        elif atclass == 'aOT':
            self.state = 2
        elif atclass == 'aSy':
            self.state = 3

    def handle_data(self, data):
        data = data.strip()
        if len(data) == 0:
            return

        if self.state == 1:
            if data == 'Brangi Brangelina':
                self.currentUser = u'Mela'
            elif data == 'Kris Jurgowski':
                self.currentUser = u'Kris'
            else:
                print data
        elif self.state == 2:
            if not self.message:
                self.message = {'name': self.currentUser, 'message': data}
            else:
                self.message['message'] += data
        elif self.state == 3:
            self.message['ts'] = data
        else:
            print data





file = open('data/Hangouts/2013-10-29.html')
parser = GTalkParser()


parser.feed(file.read().replace("<wbr>", ""))