from .tool.func import *

def recent_changes_2(conn, name, tool):
    curs = conn.cursor()

    if flask.request.method == 'POST':
        return redirect(
            '/diff/' + url_pas(name) +
            '?first=' + flask.request.form.get('b', '1') +
            '&second=' + flask.request.form.get('a', '1')
        )
    else:
        ban = ''
        select = ''
        sub = ''
        admin_6 = admin_check(6)
        admin = admin_check()
        div = '''
            <table id="main_table_set">
                <tbody>
                    <tr>
        '''

        num = int(number_check(flask.request.args.get('num', '1')))
        sql_num = (num * 50 - 50) if num * 50 > 0 else 0

        if name:
            if tool == 'history':
                sub += ' (' + load_lang('history') + ')'

                div += '''
                    <td id="main_table_width">''' + load_lang('version') + '''</td>
                    <td id="main_table_width">''' + load_lang('editor') + '''</td>
                    <td id="main_table_width">''' + load_lang('time') + '''</td>
                '''

                set_type = flask.request.args.get('set', 'normal')
                set_type = '' if set_type == 'edit' else set_type

                if set_type != 'normal':
                    curs.execute(db_change('' + \
                        'select id, title, date, ip, send, leng, hide from history ' + \
                        'where title = ? and type = ? ' + \
                        'order by id + 0 desc ' + \
                        "limit ?, 50" + \
                    ''), [name, set_type, sql_num])
                else:
                    curs.execute(db_change('' + \
                        'select id, title, date, ip, send, leng, hide from history ' + \
                        'where title = ? ' + \
                        'order by id + 0 desc ' + \
                        "limit ?, 50" + \
                    ''), [name, sql_num])

                data_list = curs.fetchall()
            else:
                div +=  '''
                    <td id="main_table_width">''' + load_lang('document_name') + '''</td>
                    <td id="main_table_width">''' + load_lang('editor') + '''</td>
                    <td id="main_table_width">''' + load_lang('time') + '''</td>
                '''

                div = '<a href="/topic_record/' + url_pas(name) + '">(' + load_lang('discussion') + ')</a><hr class=\"main_hr\">' + div

                curs.execute(db_change('' + \
                    'select id, title, date, ip, send, leng, hide from history ' + \
                    "where ip = ? order by date desc limit ?, 50" + \
                ''), [name, sql_num])
                data_list = curs.fetchall()
        else:
            div +=  '''
                <td id="main_table_width">''' + load_lang('document_name') + '''</td>
                <td id="main_table_width">''' + load_lang('editor') + '''</td>
                <td id="main_table_width">''' + load_lang('time') + '''</td>
            '''
            sub = ''
            set_type = flask.request.args.get('set', 'normal')
            set_type = '' if set_type == 'edit' else set_type

            data_list = []
            curs.execute(db_change('select id, title from rc where type = ? order by date desc'), [set_type])
            for i in curs.fetchall():
                curs.execute(db_change('select id, title, date, ip, send, leng, hide from history where id = ? and title = ?'), i)
                data_list += curs.fetchall()

        div += '</tr>'

        all_ip = ip_pas([i[3] for i in data_list])
        for data in data_list:
            select += '<option value="' + data[0] + '">' + data[0] + '</option>'
            send = '<br>'

            if data[4]:
                if not re.search(r"^(?: *)$", data[4]):
                    send = data[4]

            if re.search(r"\+", data[5]):
                leng = '<span style="color:green;">(' + data[5] + ')</span>'
            elif re.search(r"\-", data[5]):
                leng = '<span style="color:red;">(' + data[5] + ')</span>'
            else:
                leng = '<span style="color:gray;">(' + data[5] + ')</span>'

            ip = all_ip[data[3]]
            if tool == 'history':
                m_tool = '<a href="/history_tool/' + url_pas(data[1]) + '?num=' + data[0] + '&type=history">(' + load_lang('tool') + ')</a>'
            else:
                m_tool = '<a href="/history_tool/' + url_pas(data[1]) + '?num=' + data[0] + '">(' + load_lang('tool') + ')</a>'

            style = ['', '']
            date = data[2]

            if data[6] == 'O':
                if admin == 1:
                    style[0] = 'id="toron_color_grey"'
                    style[1] = 'id="toron_color_grey"'

                    send += ' (' + load_lang('hide') + ')'
                else:
                    ip = ''
                    ban = ''
                    date = ''

                    send = '(' + load_lang('hide') + ')'

                    style[0] = 'style="display: none;"'
                    style[1] = 'id="toron_color_grey"'

            if tool == 'history':
                title = '<a href="/w/' + url_pas(name) + '?num=' + data[0] + '">r' + data[0] + '</a> '
            else:
                title = '<a href="/w/' + url_pas(data[1]) + '">' + html.escape(data[1]) + '</a> '
                if int(data[0]) < 2:
                    title += '<a href="/history/' + url_pas(data[1]) + '">(r' + data[0] + ')</a> '
                else:
                    title += '<a href="/diff/' + url_pas(data[1]) + '?first=' + str(int(data[0]) - 1) + '&second=' + data[0] + '">(r' + data[0] + ')</a> '

            div += '''
                <tr ''' + style[0] + '''>
                    <td>''' + title + m_tool + ' ' + leng + '''</td>
                    <td>''' + ip + ban + '''</td>
                    <td>''' + date + '''</td>
                </tr>
                <tr ''' + style[1] + '''>
                    <td colspan="3">''' + send_parser(send) + '''</td>
                </tr>
            '''

        div += '''
                </tbody>
            </table>
        '''

        if name:
            if tool == 'history':
                div = '' + \
                    '<a href="?set=normal">(' + load_lang('normal') + ')</a> ' + \
                    '<a href="?set=edit">(' + load_lang('edit') + ')</a> ' + \
                    '<a href="?set=move">(' + load_lang('move') + ')</a> ' + \
                    '<a href="?set=delete">(' + load_lang('delete') + ')</a> ' + \
                    '<a href="?set=revert">(' + load_lang('revert') + ')</a>' + \
                    '<hr class="main_hr">' + div + \
                ''
                menu = [['w/' + url_pas(name), load_lang('return')]]
                
                if set_type == 'normal':
                    div = '''
                        <form method="post">
                            <select name="a">''' + select + '''</select> <select name="b">''' + select + '''</select>
                            <button type="submit">''' + load_lang('compare') + '''</button>
                        </form>
                        <hr class=\"main_hr\">
                    ''' + div

                    if admin == 1:
                        menu += [['add_history/' + url_pas(name), load_lang('history_add')]]

                title = name
                div += next_fix('/history/' + url_pas(name) + '?tool=' + set_type + '&num=', num, data_list)
            else:
                title = load_lang('edit_record')
                menu = [['other', load_lang('other')], ['user', load_lang('user')], ['count/' + url_pas(name), load_lang('count')]]
                div += next_fix('/record/' + url_pas(name) + '?num=', num, data_list)
        else:
            div = '' + \
                '<a href="?set=normal">(' + load_lang('normal') + ')</a> ' + \
                '<a href="?set=edit">(' + load_lang('edit') + ')</a> ' + \
                '<a href="?set=user">(' + load_lang('user_document') + ')</a> ' + \
                '<a href="?set=move">(' + load_lang('move') + ')</a> ' + \
                '<a href="?set=delete">(' + load_lang('delete') + ')</a> ' + \
                '<a href="?set=revert">(' + load_lang('revert') + ')</a>' + \
                '<hr class="main_hr">' + div + \
            ''

            menu = 0
            title = load_lang('recent_change')

        if sub == '':
            sub = 0

        return easy_minify(flask.render_template(skin_check(),
            imp = [title, wiki_set(), custom(), other2([sub, 0])],
            data = div,
            menu = menu
        ))