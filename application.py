from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/project1")
def project1():
    return render_template("project1.html")

@app.route("/project2")
def project2():
    return render_template("project2.html")

@app.route("/project3")
def project3():
    return render_template("project3.html")


# @app.route("/prject1_journey")
# def prject1_journey():
#     vnapp=request.args.get("visitor")
#     return render_template("prject1_journey.html", VisNam=vnapp)


if __name__=="__main__":
    # app.run()
    app.run(debug=True)