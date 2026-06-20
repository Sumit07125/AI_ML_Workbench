from flask import Flask,render_template,url_for,request , jsonify

app = Flask(__name__,static_folder="static",template_folder="templates")

@app.route("/login",methods=["GET","POST"])
def hello_world():
    if request.method == "POST":
        name = request.form['username']
        friends = ["sumit", "Durvesh", "Prasad","Deepak"]
        header = "<header> My City is Dhule</header>"
        return  render_template("welcome.html",name = name, friends = friends , header = header)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)