from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc
from flask_migrate import Migrate 
import pytz
from datetime import datetime


app = Flask(__name__)

db = SQLAlchemy()
DB_INFO = {
        'user': 'oyamaeiji', #登録ユーザ名: ユーザ名(hoshi) or postgres
        'password': '', #パスワード: Macのローカルの場合空白でもOK
        'host': 'localhost',
        'name': 'nba_app' #DBの名前
}
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg://{user}:{password}@{host}/{name}'.format(**DB_INFO)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
db.init_app(app)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)             # id
    full_name = db.Column(db.String(100), nullable=False)    # チーム名（フル）
    abbreviation = db.Column(db.String(100), nullable=True)  # 略称
    nickname = db.Column(db.String(100), nullable=True)      # ニックネーム
    city = db.Column(db.String(100), nullable=True)          # 拠点
    state = db.Column(db.String(100), nullable=True)         # 州
    founded = db.Column(db.String(4), nullable=True)         # 設立年
    tokyo_timzone = pytz.timezone('Asia/Tokyo')
    created_at = db.Column(db.DateTime,nullable=False,default=datetime.now(tokyo_timzone)) # 作成日時


migrate = Migrate(app, db) 


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/team")
def team_list():
    teams = Team.query.order_by(asc(Team.id)).all()
    return render_template("team_list.html", teams=teams)

@app.route("/team/<int:team_id>")
def player_list(team_id):
    return print("")