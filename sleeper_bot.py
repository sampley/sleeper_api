from urllib import request as request
from json import loads as convert2dict

def main():
    league_name = 'Keeping It Real'
    league_name = 'TestLeague'
    api_header = 'https://api.sleeper.app/v1/'
    
    #get user_id
    url = api_header + 'user/therealsampley'
    user_info = convert2dict(request.urlopen(url).read())
    user_id = user_info['user_id']
    
    # user_id: 726651407985401856
    
    url = api_header + 'user/' + user_id + '/leagues/nfl/2021'
    league = {}
    for _league in convert2dict(request.urlopen(url).read()):
        if(_league['name'] == league_name):
            league = _league
    league_id = league['league_id']
    
    url = api_header + 'league/' + league_id + '/drafts'
    draft_info = convert2dict(request.urlopen(url).read())
    print(draft_info)
    draft_id = draft_info[0]['draft_id']
    
    #GET https://api.sleeper.app/v1/draft/<draft_id>/picks
    url = api_header + 'draft/' + draft_id + '/picks'
    print(convert2dict(request.urlopen(url).read()))



    
main()