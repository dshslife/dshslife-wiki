from .tool.func import *

def login_pw_change_2(conn):
    curs = conn.cursor()

    if ban_check() == 1:
        return re_error('/ban')

    ip = ip_check()
    if ip_or_user(ip) != 0:
        return redirect('/login')

    if flask.request.method == 'POST':
        now_pw = flask.request.form.get('pw4', None)
        new_pw = flask.request.form.get('pw2', None)
        re_pw = flask.request.form.get('pw3', None)
        if now_pw and new_pw and re_pw:
            if new_pw != re_pw:
                return re_error('/error/20')

            curs.execute(db_change("select pw, encode from user where id = ?"), [flask.session['id']])
            user = curs.fetchall()
            if not user:
                return re_error('/error/2')

            if pw_check(now_pw, user[0][0], user[0][1], ip) != 1:
                return re_error('/error/10')

            curs.execute(db_change("update user set pw = ? where id = ?"), [pw_encode(new_pw), ip])

        return redirect('/user')
    else:
        return easy_minify(flask.render_template(skin_check(),
            imp = [load_lang('password_change'), wiki_set(), custom(), other2([0, 0])],
            data = '''
                <form method="post">
                    <input placeholder="''' + load_lang('now_password') + '''" name="pw4" type="password">
                    <hr class="main_hr">
                    <input placeholder="''' + load_lang('new_password') + '''" name="pw2" type="password">
                    <hr class="main_hr">
                    <input placeholder="''' + load_lang('password_confirm') + '''" name="pw3" type="password">
                    <hr class="main_hr">
                    <button type="submit">''' + load_lang('save') + '''</button>
                </form>
            ''',
            menu = [['change', load_lang('return')]]
        ))