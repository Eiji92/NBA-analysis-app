# DB設計書

## Usersテーブル
| カラム | 型 | 備考 |
|--------|----|------|
| id | INTEGER | PK |
| username | VARCHAR(50) | UNIQUE |
| password_hash | VARCHAR(200) | ハッシュ化して保存 |

## Playersテーブル
| カラム | 型 | 備考 |
|--------|----|------|
| id | INTEGER | PK |
| team_id | INTEGER | FK：Teams.id |
| fullname | VARCHAR(100) | 選手名 |
| firstname | VARCHAR(100) | 名 |
| lasttname | VARCHAR(100) | 氏 |
| is_active | BOOLEAN | 現役フラグ |

## Teamsテーブル
| カラム | 型 | 備考 |
|--------|----|------|
| id | INTEGER | PK |
| fullname | VARCHAR(100) | 選手名 |
| firstname | VARCHAR(100) | チーム名 |
| nickname | VARCHAR(100) | ニックネーム |
| city | VARCHAR(100) | 拠点 |
| state | VARCHAR(100) | 州 |
| founded | VARCHAR(4) | 設立年 |


## FavoritePlayersテーブル
| カラム | 型 | 備考 |
|--------|----|------|
| id | INTEGER | PK |
| user_id | INTEGER | FK: Users.id |
| player_id | INTEGER | NBA APIの選手ID |
| player_name | VARCHAR(100) | 選手名 |
| team_id | INTEGER | チームID |
| team_name | VARCHAR(50) | チーム名 |
| position | VARCHAR(10) | ポジション |

## PlayerStatsテーブル（スタッツをAPIから呼び出した際に登録するテーブル）
| カラム       | 型           | 備考                                      |
|-------------|-------------|------------------------------------------|
| id          | INTEGER     | PK                                       |
| player_id   | INTEGER     | FK: FavoritePlayers.player_id または Players.player_id |
| season      | VARCHAR(10) | シーズン名（例: 2023-24）               |
| points      | FLOAT       | 平均得点（PTS）                          |
| assists     | FLOAT       | 平均アシスト（AST）                      |
| rebounds    | FLOAT       | 平均リバウンド（REB）                     |
| steals      | FLOAT       | 平均スティール（STL）                     |
| blocks      | FLOAT       | 平均ブロック（BLK）                       |
| turnovers   | FLOAT       | 平均ターンオーバー（TO）                  |
| games_played| INTEGER     | 出場試合数                               |


## ER図（簡易）
別紙「er_diagram.png」参照