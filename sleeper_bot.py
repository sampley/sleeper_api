#!/usr/bin/python3
from urllib import request as request
from json import loads as j_loads
import pandas as pd
from natsort import natsorted #not really essential can remove later

def GetUserIdFromName(uname):
    url = 'https://api.sleeper.app/v1/user/' + uname
    print('API CALL: ' + url)
    return j_loads(request.urlopen(url).read())['user_id']

def GetLeagueId(user_id, league_name):
    url = 'https://api.sleeper.app/v1/user/' + user_id + '/leagues/nfl/2021'
    print('API CALL: ' + url)
    
    df = pd.DataFrame(j_loads(request.urlopen(url).read()))
    return df.loc[df.name == league_name].league_id[0]

def GetLeagueUsers(league_id):
    url = 'https://api.sleeper.app/v1/league/' + league_id + '/users'
    print('API CALL: ' + url)
    df = pd.DataFrame(j_loads(request.urlopen(url).read()))
    print(df.loc[:,['display_name', 'user_id']])
    return df
    
def GetCurrentDraftInfo(league_id):
    # test league id: 731212395778777088
    url = 'https://api.sleeper.app/v1/league/' + league_id + '/drafts'
    print('API CALL: ' + url)
    
    df = pd.DataFrame(j_loads(request.urlopen(url).read()))
    df.season = pd.to_numeric(df.season)
        
    return df.loc[df['season'] == df['season'].max()]
    
def GetDraftPicks(draft_id, league_users, players):
    url = 'https://api.sleeper.app/v1/draft/' + draft_id + '/picks'
    print('API CALL: ' + url)
    df  = pd.DataFrame(j_loads(request.urlopen(url).read()))
      
    # adding display name to the draft picks
    df['picked_by_name'] = df.picked_by
    for idx, user in league_users.iterrows():
        df.loc[(df.picked_by == user.user_id), 'picked_by_name'] = user.display_name
        
    # better to create player's name by iterrating over each row
    df['player_name'] = df.player_id
    for idx, row in df.iterrows():
        df.at[idx, 'player_name'] = players[row.player_id].full_name if players[row.player_id].full_name else row.player_id + ' D/ST'
        
    # filling nan's with empty strings
    df = df.fillna('')
    
    #df.to_excel("DraftPicks.xlsx")
    return df
    
def GetAllPlayers():
    url = 'https://api.sleeper.app/v1/players/nfl'
    print('API CALL: ' + url)
    
    df = pd.DataFrame(j_loads(request.urlopen(url).read()))
    df = df[natsorted(df.columns)]  #this isn't really needed, just makes the excel file look better
    df = df.fillna('')
    #df.to_excel("NflPlayers.xlsx")
    return df


def DoWork():
    league_name = 'Keeping It Real'
    league_name = 'TestLeague'   
    
    # user_id: 726651407985401856 <- my user id
    user_id = GetUserIdFromName('therealsampley')
    
    players = GetAllPlayers()
    league_id = GetLeagueId(user_id, league_name)
    league_users = GetLeagueUsers(league_id)
    draft_info = GetCurrentDraftInfo(league_id)
    draft_picks = GetDraftPicks(draft_info.draft_id[0], league_users, players)
    
    # this is a subset of only the players that were drafted
    drafted_players = players[draft_picks.player_id]
    
    return user_id, league_id, draft_info, draft_picks, league_users, players, drafted_players

def main():
    # just made it like this so that I can call DoWork when the script is ran in interactive mode
    DoWork()

if __name__ == 'main':
    main()
