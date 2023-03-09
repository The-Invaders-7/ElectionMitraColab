from flask import Flask, request, render_template
import os
import json 

# from werkzeug import secure_filename
app = Flask(__name__)

CROPPED_IMG_PATH = ".\\static\\FILES\\CROPPED_IMG"
upload_path = ".\\static\\FILES\\PROCESSING_FILE"

with open("information.json") as file:
    info = json.load(file)

@app.route("/")
def home():
    return render_template("index.html")

status = "fail"
@app.route("/upload", methods = ["POST"])
def upload():
    if(request.method == "POST"):
        file = request.files["my_file"]
        path = os.path.join(upload_path, file.filename)
        file.save(path)
        status = "success"
    return render_template("success.html", state = status, location = path)

@app.route("/result")
def result():
    return render_template("result.html", image = os.listdir(CROPPED_IMG_PATH), info= info)

if(__name__=="__main__"):
    app.run(debug=True)