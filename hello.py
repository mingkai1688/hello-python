import os
import uuid
from flask import Flask


app = Flask(__name__)
my_uuid = str(uuid.uuid1())
BLUE = "#0099FF"
GREEN = "#33CC33"

COLOR = GREEN

@app.route('/')
def hello():


    return """
    <html>
    <body bgcolor="{}">

    <center><h1><font color="white">Hi, I'm GUID:<br/>
    {}</br>


    </center>

    </body>
    </html>
    """.format(COLOR,my_uuid,)

if __name__ == "__main__":
	app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
