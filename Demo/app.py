from flask import Flask, render_template, request
# we will be using postgres database
# normally psycopg2 is used to access pstgres sql db
# but more commonly used library when operating with postgres sql db in flask is SQLAlchemy
# SQLAlchemy is more higher level than psycopg2
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/number_collector'
db = SQLAlchemy(app)


class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)

    email_ = db.Column(db.String(120), unique=True)
    # we don't want same id again in db
    # that's why unique is true
    number_ = db.Column(db.Integer)

    def __init__(self, email_, number_):
        self.email_ = email_
        self.number_ = number_


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/success", methods=['POST'])
def success():
    if request.method == 'POST':
        email = request.form["email_name"]
        number = request.form["number_name"]
        if db.session.query(Data).filter(Data.email_ == email).count() == 0:
            data = Data(email, number)
            db.session.add(data)
            db.session.commit()
            return render_template("success.html")
    return render_template('index.html', text="Seems like we got something from that email once!")


if __name__ == "__main__":
    app.debug = True
    app.run()
