from flask import Flask, send_file , render_template, request, redirect, session, url_for
import logging
import os
from main import search, create_SOLFile
from ChatGPT_main import search as ChatGPT_search
from ChatGPT_main import advanced_search as ChatGPT_advanced_search
from ChatGPT_main import create_SOLFile as ChatGPT_create_SOLFile

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
            bard_api_key = request.form.get("bard_api_key") # retrieve API key
            chatgpt_api_key = request.form.get("chatgpt_api_key") # retrieve API secret key
            user_input = request.form.get("user_input") # retrieve query
            llm_option = request.form.get("llm_option") # retrieve LLM option
            session["user_input"] = user_input
            session["llm_option"] = llm_option
            with open("key.py", "w") as f:
                f.write(f"Bard_Key = '{bard_api_key}'\n")
                f.write(f"OpenAi_Key = '{chatgpt_api_key}'\n")
            return redirect(url_for("result"))
        except Exception as e:
            logging.error(str(e))
            return render_template("error.html")
        
    else:
        return render_template("start.html")
    


@app.route("/newPrompt_ChatGPT", methods=["GET", "POST"])
def newPrompt_ChatGPT():
    if request.method == "POST":
        try:
            user_input = request.form.get("user_input")
            session["user_input"] = user_input
            message = ChatGPT_advanced_search(user_input)
            print("------>", message)
            return render_template("result_ChatGPT.html", user_input=user_input, message=message)
        except Exception as e:
            logging.error(str(e))
            return render_template("error.html")
        
    else:
        return render_template("newPrompt_ChatGPT.html")

@app.route("/result")
def result():
    user_input = session.get("user_input")
    llm_option = session.get("llm_option")
    print("------>", llm_option)

    if user_input:
        if llm_option == "Bard":
            message = search(user_input)
            return render_template("result.html", user_input=user_input, message=message)
        elif llm_option == "ChatGPT":
            message = ChatGPT_search(user_input)
            return render_template("result_ChatGPT.html", user_input=user_input, message=message)
        
    else:
        return redirect(url_for("user_input"))
    
@app.route("/create_solFile", methods=["GET", "POST"])
def return_SOLFile():
    llm_option = session.get("llm_option")
    if llm_option == "Bard":
        filename = create_SOLFile()
        filename = filename.replace("./Contracts/", "")
        return render_template("solFile.html", filename=filename)
    
    if llm_option == "ChatGPT":
        filename = ChatGPT_create_SOLFile()
        filename = filename.replace("./Contracts/", "")
        return render_template("solFile.html", filename=filename)


@app.route("/download_SOLFile/<filename>")
def download_SOLFile(filename):
    file_path = os.path.join(app.root_path, "Contracts", filename)

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name=filename)
    
    else:
        return "File not found"
    

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3003)
