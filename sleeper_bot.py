  
from urllib import request as request
from json import loads as j_loads
import pandas as pd

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
    url = 'https://api.sleeper.app/v1/league' + league_id + '/users'
    print('API CALL: ' + url)
    return pd.DataFrame(j_loads(request.urlopen(url).read()))
    
def GetCurrentDraftInfo(league_id):
    # test league id: 731212395778777088
    url = 'https://api.sleeper.app/v1/league/' + league_id + '/drafts'
    print('API CALL: ' + url)
    
    drafts_df = pd.DataFrame(j_loads(request.urlopen(url).read()))
    drafts_df.season = pd.to_numeric(drafts_df.season)
        
    return drafts_df.loc[drafts_df['season'] == drafts_df['season'].max()]
    
def GetDraftPicks(draft_id):
    url = 'https://api.sleeper.app/v1/draft/' + draft_id + '/picks'
    print('API CALL: ' + url)
    df  = pd.DataFrame(j_loads(request.urlopen(url).read()))
    df.to_excel("DraftPicks.xlsx")

def main():
    league_name = 'Keeping It Real'
    league_name = 'TestLeague'   
    
    # user_id: 726651407985401856 <- my user id
    user_id = GetUserIdFromName('therealsampley')
    
    league_id = GetLeagueId(user_id, league_name)
    draft_info = GetCurrentDraftInfo(league_id)
    draft_picks = GetDraftPicks(draft_info.draft_id[0])
    
    for _,row  in draft_picks.iterrows():
        print(row)
    



    
main()
