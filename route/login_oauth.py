from .tool.func import *

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient.discovery import build

def oauth_login_2(conn):
    curs = conn.cursor()

    ip = ip_check()
    if ip_or_user(ip) == 0:
        return redirect('/user')

    if ban_check(None, 'login') == 1:
        return re_error('/ban')

    if flask.request.method == 'GET':
        secret_path = os.path.join('/app/', 'client_secrets.json')
        store = Storage(secret_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(credential_path, ['https://www.googleapis.com/auth/userinfo.profile'])
            credentials = tools.run_flow(flow, store)
        else:
            return re_error('/error/10')

        user_info_service = build('oauth2', 'v2', credentials=credentials)
        user_info = user_info_service.userinfo().get().execute()
        flask.session['id'] = user_info['email']

        ua_plus(user_info['email'], ip, user_agent, get_time())
        conn.commit()

        return redirect('/user')
