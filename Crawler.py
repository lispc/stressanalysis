from weibo import APIClient

def WeiboCrawler(Uid, Access_token, Expires_in, APP_KEY, APP_SECRET, CALLBACK_URL):
    #print "test"
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    client.set_access_token(Access_token, Expires_in)
    weibo= client.statuses.user_timeline.get(uid=Uid)
    userinfo=client.users.show.get(uid=Uid)
    friendsinfo=client.friendships.groups.get(access_token=Access_token)
    
    return (weibo, userinfo, friendsinfo)

if __name__ == '__main__':
    
    APP_KEY = '118376207'
    APP_SECRET = '3b73b187a4239d2b773537d8bdb77b8e'
    CALLBACK_URL = 'http://www.stressanalyser.com'
    
    #client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    """
    code=""
    r = client.request_access_token(code)
    uid = r.uid
    access_token = r.access_token
    expires_in = r.expires_in
    """
    #"access_token":"2.00r8ggvC06XASOcf51544ebfzpM32C","remind_in":"7815262","expires_in":7815262,"uid":"2684689767"
    (w, u, f)=WeiboCrawler(2684689767, "2.00r8ggvC06XASOcf51544ebfzpM32C", 7815262, APP_KEY, APP_SECRET, CALLBACK_URL)
    print w.total_number
    print u.location
    for li in f.lists:
        print li.name
    