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
        except:
            flash("Please upload file")
            status = "fail"

        District = request.form['pdfDistrict']
        City = request.form["pdfCity"]
        Ward = request.form["pdfWard"]

        if District == "" or City == "" or Ward == "":
            flash("Fill information properly")
            status = "fail"

        if status == "fail":
                return render_template("index.html")

        print("Arguments: ", District, City, Ward, end="\n\n")
        path = os.path.join(upload_path, file.filename)
        file.save(path)
    return render_template("success.html", state = status, location = path)

@app.route("/result")
def result():
    return render_template("result.html", image = os.listdir(CROPPED_IMG_PATH), info= info)

@app.route("/output",  methods = ['GET'])
def output():
        process = subprocess.Popen(
            ['python','test.py'],
            shell=True,
            stdout=subprocess.PIPE
        )

        for line in iter(process.stdout.readline, ''):
            temp = line.rstrip() 
            time.sleep(0.1)
            yield (bytes(temp))


if(__name__=="__main__"):
    app.run(debug=True)
