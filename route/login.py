from .tool.func import *

def login_2(conn):
    curs = conn.cursor()

    ip = ip_check()
    if ip_or_user(ip) == 0:
        return redirect('/user')

    if ban_check(None, 'login') == 1:
        return re_error('/ban')

    if flask.request.method == 'POST':
        if captcha_post(flask.request.form.get('g-recaptcha-response', flask.request.form.get('g-recaptcha', ''))) == 1:
            return re_error('/error/13')
        else:
            captcha_post('', 0)

        user_agent = flask.request.headers.get('User-Agent', '')
        user_id = flask.request.form.get('id', '')

        curs.execute(db_change("select pw, encode from user where id = ?"), [user_id])
        user = curs.fetchall()
        if not user:
            return re_error('/error/2')

        pw_check_d = pw_check(
            flask.request.form.get('pw', ''),
            user[0][0],
            user[0][1],
            user_id
        )
        if pw_check_d != 1:
            return re_error('/error/10')

        curs.execute(db_change('select data from user_set where name = "2fa" and id = ?'), [user_id])
        fa_data = curs.fetchall()
        if fa_data and fa_data[0][0] != '':
            flask.session['b_id'] = user_id

            return redirect('/2fa_login')
        else:
            flask.session['id'] = user_id

            ua_plus(user_id, ip, user_agent, get_time())
            conn.commit()

            return redirect('/user')
    else:
        return easy_minify(flask.render_template(skin_check(),
            imp = [load_lang('login'), wiki_set(), custom(), other2([0, 0])],
            data =  '''
                    <a href="/oauth_login"><button style="border-radius:5px; width: 180px; background-color: rgb(247, 247, 247); height: 50px; border: 0.1px solid rgb(230, 230, 230); line-height: 30px; padding: 10px;   box-shadow: 0px 0px 20px -20px black; font-weight:700; font-size:15px;"><img src="https://i.pinimg.com/originals/39/21/6d/39216d73519bca962bd4a01f3e8f4a4b.png" alt="구글 로고" style="width: 30px;  float: left;">구글 로그인</button></a>
                    ''',
            menu = [['user', load_lang('return')]]
        ))
