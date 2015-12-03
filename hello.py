import os
import uuid
import socket
import urlparse
import redis
import json
import random
import feedparser

from flask import Flask
from yahoo_finance import Share


app = Flask(__name__)
my_uuid = str(uuid.uuid1())
BLUE = "#0099FF"
RED = "#FF0000"
GREEN = "#33CC33"

#get EMC Stock price
emc_stock = Share('EMC').get_price()

#connect to Redis service; check first if it's local testing.....
if os.environ.get('RUN_MODE') == "LOCAL":
	print "Local run mode....."
	credentials = {'hostname' : 'pub-redis-18273.us-east-1-3.3.ec2.garantiadata.com', 'port' : '18273', 'password' : 'L9Qx9o5kZUBmpAGz'}
	inst_id = '0'
	dea_ip = socket.gethostbyname(socket.gethostname())
	print dea_ip,inst_id
else:
	rediscloud_service = json.loads(os.environ['VCAP_SERVICES'])['rediscloud'][0]
	credentials = rediscloud_service['credentials']

	#get instance id and DEA IP
	#inst_id = json.loads(os.environ['VCAP_APPLICATION'])['instance_id']
	inst_id = os.environ['CF_INSTANCE_INDEX']
	dea_ip = os.environ['CF_INSTANCE_IP']

r = redis.Redis(host=credentials['hostname'], port=credentials['port'], password=credentials['password'])

## clean up redis counters...
if inst_id == '0':
	#I am the first instance.... I assume inst_id > 0 are stale
    	for stale in r.scan_iter(match='*-mingkai-counter'):
  		r.delete(stale)

#unique counter for each instance
instance_counter = inst_id+'-mingkai-counter'
r.set(instance_counter,0)

### get rss feed
d = feedparser.parse('http://feeds.feedburner.com/typepad/dsAV?format=xml')

rss = ''
for i in xrange(1,len(d['entries'])):
       rss += "<a href ='"+d['entries'][i]['link']+"'>"+d['entries'][i]['title']+'</a><br>'


#### ASCII ART STUFF
letterforms = '''\
       |       |       |       |       |       |       | |
  XXX  |  XXX  |  XXX  |   X   |       |  XXX  |  XXX  |!|
  X  X |  X  X |  X  X |       |       |       |       |"|
  X X  |  X X  |XXXXXXX|  X X  |XXXXXXX|  X X  |  X X  |#|
 XXXXX |X  X  X|X  X   | XXXXX |   X  X|X  X  X| XXXXX |$|
XXX   X|X X  X |XXX X  |   X   |  X XXX| X  X X|X   XXX|%|
  XX   | X  X  |  XX   | XXX   |X   X X|X    X | XXX  X|&|
  XXX  |  XXX  |   X   |  X    |       |       |       |'|
   XX  |  X    | X     | X     | X     |  X    |   XX  |(|
  XX   |    X  |     X |     X |     X |    X  |  XX   |)|
       | X   X |  X X  |XXXXXXX|  X X  | X   X |       |*|
       |   X   |   X   | XXXXX |   X   |   X   |       |+|
       |       |       |  XXX  |  XXX  |   X   |  X    |,|
       |       |       | XXXXX |       |       |       |-|
       |       |       |       |  XXX  |  XXX  |  XXX  |.|
      X|     X |    X  |   X   |  X    | X     |X      |/|
  XXX  | X   X |X     X|X     X|X     X| X   X |  XXX  |0|
   X   |  XX   | X X   |   X   |   X   |   X   | XXXXX |1|
 XXXXX |X     X|      X| XXXXX |X      |X      |XXXXXXX|2|
 XXXXX |X     X|      X| XXXXX |      X|X     X| XXXXX |3|
X      |X    X |X    X |X    X |XXXXXXX|     X |     X |4|
XXXXXXX|X      |X      |XXXXXX |      X|X     X| XXXXX |5|
 XXXXX |X     X|X      |XXXXXX |X     X|X     X| XXXXX |6|
XXXXXX |X    X |    X  |   X   |  X    |  X    |  X    |7|
 XXXXX |X     X|X     X| XXXXX |X     X|X     X| XXXXX |8|
 XXXXX |X     X|X     X| XXXXXX|      X|X     X| XXXXX |9|
   X   |  XXX  |   X   |       |   X   |  XXX  |   X   |:|
  XXX  |  XXX  |       |  XXX  |  XXX  |   X   |  X    |;|
    X  |   X   |  X    | X     |  X    |   X   |    X  |<|
       |       |XXXXXXX|       |XXXXXXX|       |       |=|
  X    |   X   |    X  |     X |    X  |   X   |  X    |>|
 XXXXX |X     X|      X|   XXX |   X   |       |   X   |?|
 XXXXX |X     X|X XXX X|X XXX X|X XXXX |X      | XXXXX |@|
   X   |  X X  | X   X |X     X|XXXXXXX|X     X|X     X|A|
XXXXXX |X     X|X     X|XXXXXX |X     X|X     X|XXXXXX |B|
 XXXXX |X     X|X      |X      |X      |X     X| XXXXX |C|
XXXXXX |X     X|X     X|X     X|X     X|X     X|XXXXXX |D|
XXXXXXX|X      |X      |XXXXX  |X      |X      |XXXXXXX|E|
XXXXXXX|X      |X      |XXXXX  |X      |X      |X      |F|
 XXXXX |X     X|X      |X  XXXX|X     X|X     X| XXXXX |G|
X     X|X     X|X     X|XXXXXXX|X     X|X     X|X     X|H|
  XXX  |   X   |   X   |   X   |   X   |   X   |  XXX  |I|
      X|      X|      X|      X|X     X|X     X| XXXXX |J|
X    X |X   X  |X  X   |XXX    |X  X   |X   X  |X    X |K|
X      |X      |X      |X      |X      |X      |XXXXXXX|L|
X     X|XX   XX|X X X X|X  X  X|X     X|X     X|X     X|M|
X     X|XX    X|X X   X|X  X  X|X   X X|X    XX|X     X|N|
XXXXXXX|X     X|X     X|X     X|X     X|X     X|XXXXXXX|O|
XXXXXX |X     X|X     X|XXXXXX |X      |X      |X      |P|
 XXXXX |X     X|X     X|X     X|X   X X|X    X | XXXX X|Q|
XXXXXX |X     X|X     X|XXXXXX |X   X  |X    X |X     X|R|
 XXXXX |X     X|X      | XXXXX |      X|X     X| XXXXX |S|
XXXXXXX|   X   |   X   |   X   |   X   |   X   |   X   |T|
X     X|X     X|X     X|X     X|X     X|X     X| XXXXX |U|
X     X|X     X|X     X|X     X| X   X |  X X  |   X   |V|
X     X|X  X  X|X  X  X|X  X  X|X  X  X|X  X  X| XX XX |W|
X     X| X   X |  X X  |   X   |  X X  | X   X |X     X|X|
X     X| X   X |  X X  |   X   |   X   |   X   |   X   |Y|
XXXXXXX|     X |    X  |   X   |  X    | X     |XXXXXXX|Z|
 XXXXX | X     | X     | X     | X     | X     | XXXXX |[|
X      | X     |  X    |   X   |    X  |     X |      X|\|
 XXXXX |     X |     X |     X |     X |     X | XXXXX |]|
   X   |  X X  | X   X |       |       |       |       |^|
       |       |       |       |       |       |XXXXXXX|_|
       |  XXX  |  XXX  |   X   |    X  |       |       |`|
       |   XX  |  X  X | X    X| XXXXXX| X    X| X    X|a|
       | XXXXX | X    X| XXXXX | X    X| X    X| XXXXX |b|
       |  XXXX | X    X| X     | X     | X    X|  XXXX |c|
       | XXXXX | X    X| X    X| X    X| X    X| XXXXX |d|
       | XXXXXX| X     | XXXXX | X     | X     | XXXXXX|e|
       | XXXXXX| X     | XXXXX | X     | X     | X     |f|
       |  XXXX | X    X| X     | X  XXX| X    X|  XXXX |g|
       | X    X| X    X| XXXXXX| X    X| X    X| X    X|h|
       |    X  |    X  |    X  |    X  |    X  |    X  |i|
       |      X|      X|      X|      X| X    X|  XXXX |j|
       | X    X| X   X | XXXX  | X  X  | X   X | X    X|k|
       | X     | X     | X     | X     | X     | XXXXXX|l|
       | X    X| XX  XX| X XX X| X    X| X    X| X    X|m|
       | X    X| XX   X| X X  X| X  X X| X   XX| X    X|n|
       |  XXXX | X    X| X    X| X    X| X    X|  XXXX |o|
       | XXXXX | X    X| X    X| XXXXX | X     | X     |p|
       |  XXXX | X    X| X    X| X  X X| X   X |  XXX X|q|
       | XXXXX | X    X| X    X| XXXXX | X   X | X    X|r|
       |  XXXX | X     |  XXXX |      X| X    X|  XXXX |s|
       |  XXXXX|    X  |    X  |    X  |    X  |    X  |t|
       | X    X| X    X| X    X| X    X| X    X|  XXXX |u|
       | X    X| X    X| X    X| X    X|  X  X |   XX  |v|
       | X    X| X    X| X    X| X XX X| XX  XX| X    X|w|
       | X    X|  X  X |   XX  |   XX  |  X  X | X    X|x|
       |  X   X|   X X |    X  |    X  |    X  |    X  |y|
       | XXXXXX|     X |    X  |   X   |  X    | XXXXXX|z|
  XXX  | X     | X     |XX     | X     | X     |  XXX  |{|
   X   |   X   |   X   |       |   X   |   X   |   X   |||
  XXX  |     X |     X |     XX|     X |     X |  XXX  |}|
 XX    |X  X  X|    XX |       |       |       |       |~|
'''.splitlines()

table = {}
for form in letterforms:
    if '|' in form:
        table[form[-2]] = form[:-3].split('|')
ROWS = len(table.values()[0])

def horizontal(word):
    text = '<pre>'
    for row in range(ROWS):
        for c in word:
            text += table[c][row]
            text += ' '
        text += ' \n'
    text += '\n</pre>'
    return text

@app.route('/')
def hello(): 
    total_count = 0
    instance_count = 0
    r.incr(instance_counter)
    count = r.get(instance_counter)

    if int(count) > 10:
	extra = 'Are you so bored? You have clicked this instance alone '+str(count)+' times???... Get a life!!!'
    else:
        extra = 'Access count for this instance is : '+ count


    if int(count) % 2 == 0:
        COLOR = 'rgb('+str(random.randint(0,255))+',0,28)'
    else:
        COLOR = 'rgb(0,'+str(random.randint(0,255))+',28)'

    for sum in r.scan_iter(match='*-counter'):
  	total_count += int(r.get(sum))
        instance_count += 1
   
    extra += '<br><font size=6>Total access count across all '
    extra += str(instance_count)
    extra += ' instances is : '
    extra += str(total_count)
    extra += '</font><br><br><i>BTW, while you were mucking around.... the EMC stock price has gone to USD '
    extra += emc_stock
    extra += '</i>'
 
    footer = horizontal('EMC Dev Ops Geek Week')

    return """
    <html>
    <body bgcolor="{}">

    <center><h1><font color="white">Hi, I'm GUID:
    {} on host {}<br>
    <h3>I am also actually application instance {} on DEA with IP {}</h3>
    <br><br>
    {}
    <br><br><br><font size=3>Using redis server at {} on port {}</font>
    </center>
    {}
    Recommended reading if you are really bored......<br>
    {}
    </body>
    </html>
    """.format(COLOR,my_uuid,socket.gethostname(),inst_id,dea_ip,extra,credentials['hostname'],credentials['port'],footer,rss)

if __name__ == "__main__":
	app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
