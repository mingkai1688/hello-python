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

#connect to Redis service; check first if it's local testing.....
if os.environ['RUN_MODE'] == "LOCAL":
	print "Local run mode....."
	credentials = {'hostname' : 'pub-redis-11211.us-east-1-2.2.ec2.garantiadata.com', 'port' : '11211', 'password' : 'p99stMa1OGxUEhDP'}
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

#unique counter for each instance
instance_counter = inst_id+'-counter'
r.set(instance_counter,0)


@app.route('/')
def hello(): 
    total_count = 0
    instance_count = 0
    r.incr(instance_counter)
    count = r.get(instance_counter)

    if int(count) > 10:
	extra = '<h3>Are you so bored? You have clicked this instance alone '+str(count)+' times???... Get a life!!!</h3>'
    else:
        extra = 'Count is : '+ count

    if int(count) % 2 == 0:
        COLOR = BLUE
    else:
        COLOR = RED

    for sum in r.scan_iter(match='*-counter'):
  	total_count += int(r.get(sum))
        instance_count += 1
   

    return """
    <html>
    <body bgcolor="{}">

    <center><h1><font color="white">Hi, I'm GUID:<br/>
    {} on host {}</br>
    <h2>I am actually instance {} on DEA with IP {}</h2>
    <br><br>
    {}
    <h3>Total count across all {} instances is : {}</h3>
    <h3>Using redis server at {} on port {}</h3>
    </center>

    </body>
    </html>
    """.format(COLOR,my_uuid,socket.gethostname(),inst_id,dea_ip,extra,instance_count,total_count,credentials['hostname'],credentials['port'])

if __name__ == "__main__":
	app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
