from .tool.func import *

from oauthlib.oauth2 import WebApplicationClient
import requests

def oauth_login_2(conn):
    curs = conn.cursor()

    ip = ip_check()
    if ip_or_user(ip) == 0:
        return redirect('/user')

    if ban_check(None, 'login') == 1:
        return re_error('/ban')

    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "540478836154-6679hsues6alukbbabebuerg3he2ho70.apps.googleusercontent.com")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "I5pxRXTYsnPJyEie0khfG17t")
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )

    client = WebApplicationClient(GOOGLE_CLIENT_ID)

    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "_callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)
