from flask import Flask,current_app, send_from_directory, render_template, request, redirect, session, url_for
import logging
import os
from main import search, create_SOLFile


app = Flask(__name__)
app.secret_key = 'mysecretkey'


@app.route("/")
def index():
    logging.info("Welcome to the Flask app!")
    return redirect(url_for("user_input"))

@app.route("/user_input", methods=["GET", "POST"])
def user_input():
    if request.method == "POST":
        try:
            user_input = request.form.get("user_input")
            session["user_input"] = user_input
            return redirect(url_for("result"))
        except Exception as e:
            logging.error(str(e))
            return render_template("error.html")
    else:
        return render_template("start.html")


@app.route("/result")
def result():
    user_input = session.get("user_input")
    if user_input:
        message = search(user_input)
        return render_template("result.html", user_input=user_input, message=message)
    else:
        return redirect(url_for("user_input"))
    
@app.route("/create_solFile")
def return_SOLFile():
    filename = create_SOLFile()
    return render_template("solFile.html", filename=filename)


@app.route("/download_SOLFile/<filename>", methods=['GET', 'POST'])
def download_SOLFile(filename):
    # Appending app path to upload folder path within app root folder
    uploads = os.path.join(current_app.root_path, app.config['./Contracts'])
    # Returning file from appended path
    return send_from_directory(directory=uploads, filename=filename)
    

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3003)
