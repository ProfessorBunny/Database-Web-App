from flask import Flask, render_template, request
# we will be using postgres database
# normally psycopg2 is used to access pstgres sql db
# but more commonly used library when operating with postgres sql db in flask is SQLAlchemy
# SQLAlchemy is more higher level than psycopg2

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/success", methods=['POST'])
def success():
    if request.method == 'POST':
        email = request.form["email_name"]
        number = request.form["number_name"]
        return render_template("success.html")


if __name__ == "__main__":
    app.debug = True
    app.run()
