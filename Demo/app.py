from flask import Flask, render_template, request
# we will be using postgres database
# normally psycopg2 is used to access pstgres sql db
# but more commonly used library when operating with postgres sql db in flask is SQLAlchemy
# SQLAlchemy is more higher level than psycopg2
from flask_sqlalchemy import SQLAlchemy
from email.mime.text import MIMEText
import smtplib
from sqlalchemy.sql import func


def send_email(email, number, average_number, count):
    from_email = "nikunjmailer@gmail.com"
    from_password = "qwerty@123456"
    to_email = email

    subject = "The updated Number"
    message = "Hey there, your number is <strong>%s</strong>. <br> Average number by far is <strong>%s</strong> and that is calculated from the input of <strong>%s</strong> people. <br> Thanks!" % (
        number, average_number, count)

    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)


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
            average_number = db.session.query(func.avg(Data.number_)).scalar()
            average_number = round(average_number, 1)
            count = db.session.query(Data.number_).count()
            send_email(email, number, average_number, count)
            return render_template("success.html")
    return render_template('index.html', text="Seems like we already got something from this email once!")


if __name__ == "__main__":
    app.debug = True
    app.run()
