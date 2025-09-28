from nba_api.stats.static import players
from nba_api.stats.static import teams
from myapp import Team

all_players = players.get_players()
print("総選手数:", len(all_players))

# 現役選手だけ
active_players = [p for p in all_players if p["is_active"]]
print("現役選手数:", len(active_players))

# # 引退済み
# retired_players = [p for p in all_players if not p["is_active"]]
# print("引退済み:", len(retired_players))


# all_teams = teams.get_teams()
# print("総チーム数:", len(all_teams))

# print(active_players[1])

active_players2 = players.get_active_players()
print(len(active_players2))

# all_teams = teams.get_teams()
# print(all_teams)

# myapp.py
print(['SQLALCHEMY_DATABASE_URI'])
