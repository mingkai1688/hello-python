import os
import uuid
import socket
import urlparse
import redis
import json

from flask import Flask


app = Flask(__name__)
my_uuid = str(uuid.uuid1())
BLUE = "#0099FF"
RED = "#FF0000"
GREEN = "#33CC33"

COLOR = RED
#count = 0
rediscloud_service = json.loads(os.environ['VCAP_SERVICES'])['rediscloud'][0]
credentials = rediscloud_service['credentials']
r = redis.Redis(host=credentials['hostname'], port=credentials['port'], password=credentials['password'])
#redishost='pub-redis-11211.us-east-1-2.2.ec2.garantiadata.com'
#redisport='11211'
#r = redis.Redis(host=redishost, port=redisport, password='p99stMa1OGxUEhDP')

r.set('rcounter',0)

@app.route('/')
def hello(): 
    r.incr('rcounter')
    count = r.get('rcounter')
    if int(count) > 10:
	extra = '<h2>Are you so bored to click this '+str(count)+' times???... Get a life!!!</h2>'
    else:
        extra = 'Count is : '+count

    if int(count) % 2 == 0:
        COLOR = BLUE
    else:
        COLOR = RED

    return """
    <html>
    <body bgcolor="{}">

    <center><h1><font color="white">Hi, I'm GUID:<br/>
    {} on host {}</br>
    {}
    <h3>Using redis server at {} on port {}</h3>


    </center>

    </body>
    </html>
    """.format(COLOR,my_uuid,socket.gethostname(),extra,credentials['hostname'],credentials['port'])

if __name__ == "__main__":
	app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
