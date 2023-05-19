from flask import Flask, request, render_template, flash, Response, jsonify
import os
import json 
import subprocess
import time

# from werkzeug import secure_filename
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'

CROPPED_IMG_PATH = ".\\static\\FILES\\CROPPED_IMG"
upload_path = ".\\static\\FILES\\PROCESSING_FILE"

District = "District"
City = "City"
Ward = "Ward"

with open("information.json") as file:
    info = json.load(file)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods = ["POST"])
def upload():
    status = "success"
    if(request.method == "POST"):
        try:
            file = request.files["my_file"]
            path = os.path.join(upload_path, file.filename)
            file.save(path)
        except:
            flash("ERROR: Please upload file")
            status = "fail"

        District = request.form['pdfDistrict']
        City = request.form["pdfCity"]
        Ward = request.form["pdfWard"]

        if District == "" or City == "" or Ward == "":
            flash("ERROR: Fill information properly")
            status = "fail"

        if status == "fail":
                return render_template("index.html")

        command = f"python extract.py {District} {City} {Ward}"
        print("Arguments: ", District, City, Ward, end="\n\n")
    return render_template("success.html", state = status, location = path, command = command)

''''
@app.route("/result")
def result():
    return render_template("result.html", image = os.listdir(CROPPED_IMG_PATH), info= info)

@app.route("/output",  methods = ['GET'])
def output():

    yield "Processing..."
    process = subprocess.Popen(
        ['python','extract.py', str(District), str(City), str(Ward)],
        shell=True,
    )
    output = process.communicate()
    return output
'''

from flask_socketio import SocketIO
socketio = SocketIO(app)

@socketio.on('run_command')
def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in iter(process.stdout.readline, ''):
        socketio.emit('output', {'data': line.strip()})
    process.stdout.close()
    process.wait()

if(__name__=="__main__"):
    app.run(debug=True)
