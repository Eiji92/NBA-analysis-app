from myapp import db
from myapp import app,Team
from nba_api.stats.static import teams
from datetime import datetime

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