from sys import prefix

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
import os
from wtforms.validators import NumberRange


app = Flask(__name__)
db = SQLAlchemy(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/qs/temp/evo/data.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ha3d_9ue5s'


class dwg(db.Model):
    localhub = db.Column(db.String, primary_key=True)
    dwg_num = db.Column(db.String, unique=False)
    dwg_name = db.Column(db.String, unique=False)
    dwg_norm = db.Column(db.String, unique=False)

    def __init__(self, localhub, dwg_num, dwg_name, dwg_norm):
        self.localhub = localhub
        self.dwg_num = dwg_num
        self.dwg_name = dwg_name
        self.dwg_norm = dwg_norm

    def __repr__(self):
        return '<Localhub %r>' % self.localhub


class charge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rec_local = db.Column(db.String, unique=False)
    dwg_norm = db.Column(db.String, unique=False)
    dwg_num = db.Column(db.String, unique=False)
    rec_Quantity = db.Column(db.Integer, unique=False)
    type = db.Column(db.String, unique=False)

    def __init__(self, id, rec_local, dwg_norm, dwg_num, rec_Quantity, type):
        self.id = id
        self.rec_local = rec_local
        self.dwg_norm = dwg_norm
        self.dwg_num = dwg_num
        self.rec_Quantity = rec_Quantity
        self.type = type

    def __repr__(self):
        return '<id %r>' % self.id


db.create_all()


class PutSth(FlaskForm):
    m8 = IntegerField(u'大功率-普通', validators=[NumberRange(min=0, max=40)])
    m8d = IntegerField(u'大功率-防爆', validators=[NumberRange(min=0, max=40)])
    m825 = IntegerField(u'大功率-普通', validators=[NumberRange(min=0, max=2)])
    m825d = IntegerField(u'大功率-防爆', validators=[NumberRange(min=0, max=999)])
    m808 = IntegerField(u'大功率-普通', validators=[NumberRange(min=0, max=999)])
    m808d = IntegerField(u'大功率-防爆', validators=[NumberRange(min=0, max=999)])
    submit = SubmitField(u'提交')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = PutSth()
    if form.validate_on_submit():
        m8 = form.m8.data
        m8d = form.m8d.data
        m825 = form.m825.data
        m825d = form.m825d.data
        m808 = form.m808.data
        m808d = form.m808d.data
    return render_template("index.html", form=form)
# m8=0,m8d=0,m825=0,m825d=0,m808=0,m808d=0


@app.route('/search', methods=['GET', 'POST'])
def search():
    dwg1 = dwg.query.all()
    return render_template('search.html', dwg1=dwg1)


@app.route('/charge_sheet', methods=['GET', 'POST'])
def charge_sheet():
    cs_m8 = int(request.form.get('m8') or 0)
    cs_m8d = int(request.form.get('m8d') or 0)
    cs_m825 = int(request.form.get('m825') or 0)
    cs_m825d = int(request.form.get('m825d') or 0)
    cs_m808 = int(request.form.get('m808') or 0)
    cs_m808d = int(request.form.get('m808d') or 0)
    sheets = charge.query.all()
    return render_template('charge_sheet.html', sheets=sheets, cs_m8=cs_m8, cs_m8d=cs_m8d, cs_m825=cs_m825, cs_m825d=cs_m825d, cs_m808=cs_m808, cs_m808d=cs_m808d)


# 运行
if __name__ == '__main__':
    app.run(debug=True)
