from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc
from flask_migrate import Migrate 
import pytz
from datetime import datetime
from nba_api.stats.endpoints import commonplayerinfo
from flask_login import UserMixin, LoginManager,login_user,login_required, logout_user
import os 
from werkzeug.security import generate_password_hash,check_password_hash


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

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)             # id
    team_id = db.Column(db.Integer,db.ForeignKey('team.id'), nullable=False)    # チームid
    full_name = db.Column(db.String(100), nullable=False)  # フルネーム
    first_name = db.Column(db.String(100), nullable=False)      # 名
    last_name = db.Column(db.String(100), nullable=False)          # 氏
    is_active = db.Column(db.Boolean, nullable=False)         # 現役
    tokyo_timzone = pytz.timezone('Asia/Tokyo')
    created_at = db.Column(db.DateTime,nullable=False,default=datetime.now(tokyo_timzone)) # 作成日時

class User(UserMixin, db.Model):
 id = db.Column(db.Integer, primary_key=True)
 username = db.Column(db.String(30), unique=True, nullable=False)
 password = db.Column(db.String(200), unique=False, nullable=False)

migrate = Migrate(app, db) 

#①Flaskのセッション情報の暗号化等に使用
app.config["SECRET_KEY"] = os.urandom(24)

#②login管理用
login_manager = LoginManager() 
login_manager.init_app(app)  

#③現在のユーザーを識別するために必要
@login_manager.user_loader 
def load_user(user_id): 
    return User.query.get(int(user_id))



@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# ログインページ
@app.route('/login',methods=['GET','POST'])
def login():
     if request.method == 'POST':
        # ユーザーネーム、パスワードの取得
        username = request.form.get('username')
        password = request.form.get('password')
        # 取得したユーザーネームをwhere条件にDBを探す
        user = User.query.filter_by(username=username).first()
        # DBから取得したパスワードを復号し、入力したパスワードと一致したらログインする
        if check_password_hash(user.password,password=password):
             login_user(user)
             return redirect('/team')
        else:
             return render_template('login.html', msg='ユーザー名/パスワードが違います')
     return render_template('login.html', msg='')

# サインアップページ
@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_pass = generate_password_hash(password)
        user = User(username=username, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    elif request.method == 'GET':
        return render_template('signup.html')
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route("/team")
@login_required
def team_list():
    teams = Team.query.order_by(asc(Team.id)).all()
    return render_template("team_list.html", teams=teams)

@app.route("/team/<int:team_id>")
@login_required
def player_list(team_id):
    players = Player.query.filter(Player.team_id == team_id).order_by(asc(Player.full_name)).all()
    teams = Team.query.get(team_id)
    # players_info = []

    # for player in players:
    #     try:
    #         info = commonplayerinfo.CommonPlayerInfo(player_id=player.id).get_normalized_dict()
    #         position = info['CommonPlayerInfo'][0].get('POSITION', 'N/A')
    #     except Exception as e:
    #         print(f"API取得失敗: {player.full_name}, error: {e}")

    #     players_info.append({
    #         "id":player.id,
    #         "full_name":player.full_name,
    #         "position":position
    #     })
    return render_template("player_list.html", players=players, teams=teams)