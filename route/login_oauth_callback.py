from .tool.func import *

from oauthlib.oauth2 import WebApplicationClient
import requests

def oauth_login_callback_2(conn):
    curs = conn.cursor()
    ip = ip_check()

    code = flask.request.args.get("code")

    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "540478836154-6679hsues6alukbbabebuerg3he2ho70.apps.googleusercontent.com")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "I5pxRXTYsnPJyEie0khfG17t")
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )

    client = WebApplicationClient(GOOGLE_CLIENT_ID)

    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=flask.request.url,
        redirect_url=flask.request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return re_error('/error/10')

    flask.session['id'] = users_name

    user_agent = flask.request.headers.get('User-Agent')
    ua_plus(users_name, ip, user_agent, get_time())
    conn.commit()

    # Check unique id is already exist
    curs.execute(db_change('select exists(select * from user where pw = ?)'), [
        'ajwcnow3ugycowuh43xn8o7on4yogurn4oi' + unique_id,
    ])
    pw_to_check = curs.fetchall()
    print(pw_to_check[0][0])

    if pw_to_check[0] is 0: # If not exist, register user
        curs.execute(db_change('select data from other where name = "encode"'))
        db_data = curs.fetchall()
        curs.execute(db_change("insert into user (id, pw, acl, date, encode) values (?, ?, ?, ?, ?)"), [
            users_name,
            'ajwcnow3ugycowuh43xn8o7on4yogurn4oi' + unique_id,
            'user',
            get_time(),
            db_data[0][0]
        ])
        curs.execute(db_change('insert into user_set (name, id, data) values ("email", ?, ?)'), [users_name, users_email])
    return redirect('/user')