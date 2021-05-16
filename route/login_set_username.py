from .tool.func import *

def login_set_username_2(conn):
    curs = conn.cursor()
    
    if flask.request.method == 'POST':
        current_id = flask.session['id']
        new_id = flask.request.form.get('id', '')
        if new_id == '':
            return re_error('/error/37')
        
        curs.execute(db_change('select changed from user where id = ?'), [
            current_id,
        ])
        id_changed = curs.fetchall()
        if id_changed[0][0] is '1':
            return redirect('/user')

        # Check unique id is already exist
        curs.execute(db_change('select exists(select * from user where id = ?)'), [
            new_id,
        ])
        id_already = curs.fetchall()
        if id_already[0][0] is 1:
            return re_error('/error/6')

        curs.execute(db_change('update user set id=? where id=?'), [new_id, current_id])
        curs.execute(db_change('update user_set set id=? where id=?'), [new_id, current_id])
        curs.execute(db_change('update user set changed=? where id=?'), [1, current_id])
        flask.session['id'] = new_id
        return redirect('/user')
    else:
        current_id = flask.session['id']
        curs.execute(db_change('select changed from user where id = ?'), [
            current_id,
        ])
        id_changed = curs.fetchall()
        if id_changed[0][0] is '1':
            return redirect('/user')

        return easy_minify(flask.render_template(skin_check(),
            imp = [load_lang('id'), wiki_set(), custom(), other2([0, 0])],
            data = '''
                <form method="post">
                    <input placeholder="''' + load_lang('id') + '''" name="id" type="text">
                    <hr class="main_hr">
                    <button type="submit">''' + load_lang('save') + '''</button>
                </form>
            ''',
            menu = [['user', load_lang('return')]]
        ))
