from myapp import db
from myapp import app,Team,Player
from nba_api.stats.static import teams,players
from datetime import datetime
from nba_api.stats.endpoints import commonplayerinfo
import time

def teams_insert():
    """Teamsテーブルに初期データを投入"""
    if db.session.query(Team).count() > 0:
        print("Teams table already populated.")
        return

    all_teams = teams.get_teams()
    for t in all_teams:
        team = Team(
            id=t['id'],
            full_name=t['full_name'],
            abbreviation=t['abbreviation'],
            nickname=t['nickname'],
            city=t['city'],
            state=t['state'],
            founded=t['year_founded'],
            created_at=datetime.now() 
        )
        db.session.add(team)
    db.session.commit()
    print("Teams table populated!")

if __name__ == "__main__": 
    with app.app_context():
        teams_insert()

def players_insert():
    """playersテーブルに初期データを投入"""
    if db.session.query(Player).count() > 0:
        print("Players table already populated.")
        return

    all_active_players = players.get_active_players()
    for p in all_active_players:
        info = commonplayerinfo.CommonPlayerInfo(p["id"]) 
        data = info.get_normalized_dict()

        team_id = data["CommonPlayerInfo"][0]["TEAM_ID"]
        if team_id == 0:
            print(f"Skipping {p['full_name']} (no team)")
            continue

        player = Player(
            id=p['id'],
            team_id=team_id,
            full_name=p['full_name'],
            first_name=p['first_name'],
            last_name=p['last_name'],
            is_active=p['is_active'],
            created_at=datetime.now() 
        )
        db.session.add(player)
        time.sleep(0.5)

    db.session.commit()
    print("Players table populated!")

if __name__ == "__main__": 
    with app.app_context():
        players_insert()