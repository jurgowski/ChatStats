import HTMLParser

class MessageParser(HTMLParser):


html_data = open('data/messages.htm')
HTMLParser.HTMLParser.feed(html_data)

mParser = MessageParser()