import os
import uuid
import socket

from flask import Flask


app = Flask(__name__)
my_uuid = str(uuid.uuid1())
BLUE = "#0099FF"
RED = "#FF0000"
GREEN = "#33CC33"

COLOR = RED
count = 0

@app.route('/')
def hello():
    global count
    count += 1
    if count > 10:
	extra = '<h2>Are you so bored to click this '+str(count)+' times???... Get a life!!!</h2>'
    else:
	extra = ''
    return """
    <html>
    <body bgcolor="{}">

    <center><h1><font color="white">Hi, I'm GUID:<br/>
    {} on host {}</br>
    <h2>Count is : {} </h2>
    {}


    </center>

    </body>
    </html>
    """.format(COLOR,my_uuid,socket.gethostname(),count,extra)

if __name__ == "__main__":
	app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
