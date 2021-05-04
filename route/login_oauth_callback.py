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

    flask.session['id'] = users_email

    user_agent = flask.request.headers.get('User-Agent')
    ua_plus(users_email, ip, user_agent, get_time())
    conn.commit()
    return redirect('/user')