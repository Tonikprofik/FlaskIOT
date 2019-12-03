from flask import Flask
from flask import request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:tonik@localhost/iotdata'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Iotdata(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    gpsx = db.Column(db.Numeric(20, 6))
    gpsy = db.Column(db.Numeric(20, 6))
    messtype = db.Column(db.String(50))
    messvalue = db.Column(db.Numeric(20, 2))
    ts = db.Column(db.TIMESTAMP)

    def __init__(self, gpsx, gpsy, messtype, messvalue, ts):
        self.gpsx = gpsx
        self.gpsy = gpsy
        self.messtype = messtype
        self.messvalue = messvalue
        self.ts = ts

    def __repr__(self):
        return self.messtype



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route('/openlayers')
def openlayers():
    myIotdata = Iotdata.query.all()
    return render_template('openlayers.html', myIotdata=myIotdata)



@app.route('/showdata')
def showdata():
    myIotdata = Iotdata.query.all()
    return render_template('showdata.html', myIotdata=myIotdata)



@app.route('/post_data')
def post_data():
    iotdata = Iotdata(gpsx=10, gpsy=11, messtype='hello', messvalue='10', ts='2018-06-22 19:10:25-07')
    db.session.add(iotdata)
    db.session.commit()
    return "<h1 style='color: red'>hello flask - saved some data</h1>"


@app.route('/post_iotdata', methods=['POST'])
def post_iotdata():
    iotdata = Iotdata(gpsx=request.form['gpsx'], gpsy=request.form['gpsy'], messtype=request.form['messtype'], messvalue=request.form['messvalue'],
                      ts=datetime.now())
    db.session.add(iotdata)
    db.session.commit()
    return redirect(url_for('showdata'))





if __name__ == '__main__':
    app.run(debug=True)
