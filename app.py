from flask import Flask, request, render_template
import os
# from werkzeug import secure_filename
app = Flask(__name__)


upload_path = "C:\\Users\\asdha\\Desktop\\EDI-IV\\My Work\\static\\uploaded_files"

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

if(__name__=="__main__"):
    app.run(debug=True)