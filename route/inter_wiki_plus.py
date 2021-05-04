from .tool.func import *

def inter_wiki_plus_2(conn, tools, name):
    curs = conn.cursor()

    if flask.request.method == 'POST':
        if tools == 'plus_inter_wiki':
            if name:
                curs.execute(db_change("delete from html_filter where html = ? and kind = 'inter_wiki'"), [name])

            curs.execute(db_change("delete from html_filter where html = ? and kind = 'inter_wiki'"), [
                flask.request.form.get('title', 'test')
            ])
            curs.execute(db_change('insert into html_filter (html, plus, plus_t, kind) values (?, ?, ?, "inter_wiki")'), [
                flask.request.form.get('title', 'test'),
                flask.request.form.get('link', 'test'),
                flask.request.form.get('icon', '')
            ])

            admin_check(None, 'inter_wiki_plus')
        elif tools == 'plus_edit_filter':
            if admin_check(None, 'edit_filter edit') != 1:
                return re_error('/error/3')

            if flask.request.form.get('second', '0') == '0':
                end = 'X'
            else:
                end = flask.request.form.get('second', 'X')

            try:
                re.compile(flask.request.form.get('content', 'test'))

                curs.execute(db_change("delete from html_filter where html = ? and kind = 'regex_filter'"), [name])
                curs.execute(db_change("insert into html_filter (html, plus, plus_t, kind) values (?, ?, ?, 'regex_filter')"), [
                    name,
                    flask.request.form.get('content', 'test'),
                    end
                ])
            except:
                return re_error('/error/23')
        else:
            plus_d = ''

            if tools == 'plus_name_filter':
                try:
                    re.compile(flask.request.form.get('title', 'test'))
                except:
                    return re_error('/error/23')

                admin_check(None, 'name_filter edit')

                type_d = 'name'
            elif tools == 'plus_file_filter':
                try:
                    re.compile(flask.request.form.get('title', 'test'))
                except:
                    return re_error('/error/23')

                admin_check(None, 'file_filter edit')

                type_d = 'file'
            elif tools == 'plus_email_filter':
                admin_check(None, 'email_filter edit')

                type_d = 'email'
            elif tools == 'plus_image_license':
                admin_check(None, 'image_license edit')

                type_d = 'image_license'
            elif tools == 'plus_extension_filter':
                admin_check(None, 'extension_filter edit')

                type_d = 'extension'
            else:
                admin_check(None, 'edit_top edit')

                type_d = 'edit_top'
                plus_d = flask.request.form.get('markup', 'test')

            if name:
                curs.execute(db_change("delete from html_filter where html = ? and kind = ?"), [
                    name,
                    type_d
                ])

            curs.execute(db_change('insert into html_filter (html, kind, plus) values (?, ?, ?)'), [
                flask.request.form.get('title', 'test'),
                type_d,
                plus_d
            ])

        conn.commit()

        return redirect('/' + re.sub(r'^plus_', '', tools))
    else:
        get_sub = 0
        if admin_check() != 1:
            stat = 'disabled'
        else:
            stat = ''

        if tools == 'plus_inter_wiki':
            if name:
                curs.execute(db_change("select html, plus, plus_t from html_filter where html = ? and kind = 'inter_wiki'"), [name])
                exist = curs.fetchall()
                if exist:
                    value = exist[0]
                else:
                    value = ['', '', '']
            else:
                value = ['', '', '']

            title = load_lang('interwiki_add')
            form_data = '''
                ''' + load_lang('name') + '''
                <hr class="main_hr">
                <input value="''' + html.escape(value[0]) + '''" type="text" name="title">
                <hr class="main_hr">
                ''' + load_lang('link') + '''
                <hr class="main_hr">
                <input value="''' + html.escape(value[1]) + '''" type="text" name="link">
                <hr class="main_hr">
                ''' + load_lang('icon') + ''' (HTML)
                <hr class="main_hr">
                <input value="''' + html.escape(value[2]) + '''" type="text" name="icon">
            '''
        elif tools == 'plus_edit_filter':
            curs.execute(db_change("select plus, plus_t from html_filter where html = ? and kind = 'regex_filter'"), [name])
            exist = curs.fetchall()
            if exist:
                textarea = exist[0][0]

                if exist[0][1] == 'X':
                    time_check = 'checked="checked"'
                    time_data = ''
                else:
                    time_check = ''
                    time_data = exist[0][1]
            else:
                textarea = ''
                time_check = ''
                time_data = ''

            insert_data = ''
            if stat == '':
                t_data = [
                    ['86400', load_lang('1_day')],
                    ['432000‬', load_lang('5_day')],
                    ['2592000', load_lang('30_day')],
                    ['15552000', load_lang('180_day')],
                    ['31104000‬', load_lang('360_day')],
                    ['0', load_lang('limitless')]
                ]
                for i in t_data:
                    insert_data += '<a href="javascript:insert_v(\'second\', \'' + i[0] + '\')">(' + i[1] + ')</a> '

            title = load_lang('edit_filter_add')
            form_data = '''
                <script>function insert_v(name, data) { document.getElementById(name).value = data; }</script>''' + insert_data + '''
                <hr class="main_hr">
                <input ''' + stat + ''' placeholder="''' + load_lang('second') + '''" id="second" name="second" type="text" value="''' + html.escape(time_data) + '''">
                <hr class="main_hr">
                <input ''' + stat + ''' placeholder="''' + load_lang('regex') + '''" name="content" value="''' + html.escape(textarea) + '''" type="text">
            '''
        elif tools == 'plus_name_filter':
            title = load_lang('id_filter_add')
            form_data = '' + \
                load_lang('regex') + \
                '<hr class="main_hr">' + \
                '<input value="' + html.escape(name if name else '') + '" type="text" name="title">' + \
            ''
        elif tools == 'plus_file_filter':
            title = load_lang('file_filter_add')
            form_data = '' + \
                load_lang('regex') + \
                '<hr class="main_hr">' + \
                '<input value="' + html.escape(name if name else '') + '" type="text" name="title">' + \
            ''
        elif tools == 'plus_email_filter':
            title = load_lang('email_filter_add')
            form_data = '' + \
                load_lang('email') + \
                '<hr class="main_hr">' + \
                '<input value="' + html.escape(name if name else '') + '" type="text" name="title">' + \
            ''
        elif tools == 'plus_image_license':
            title = load_lang('image_license_add')
            form_data = '' + \
                load_lang('license') + \
                '<hr class="main_hr">' + \
                '<input value="' + html.escape(name if name else '') + '" type="text" name="title">' + \
            ''
        elif tools == 'plus_extension_filter':
            title = load_lang('extension_filter_add')
            form_data = '' + \
                load_lang('extension') + \
                '<hr class="main_hr">' + \
                '<input value="' + html.escape(name if name else '') + '" type="text" name="title">' + \
            ''
        else:
            title = load_lang('edit_tool_add')
            if name:
                curs.execute(db_change("select plus from html_filter where html = ? and kind = 'edit_top'"), [name])
                exist = curs.fetchall()
                if exist:
                    value = exist[0][0]
                else:
                    value = ''
            else:
                value = ''

            form_data = '''
                ''' + load_lang('title') + '''
                <hr class="main_hr">
                <input value="''' + html.escape(name if name else '') + '''" type="text" name="title">
                <hr class="main_hr">
                ''' + load_lang('markup') + '''
                <hr class="main_hr">
                <input value="''' + html.escape(value) + '''" type="text" name="markup">
            '''

        return easy_minify(flask.render_template(skin_check(),
            imp = [title, wiki_set(), custom(), other2([get_sub, 0])],
            data =  '''
                    <form method="post">
                        ''' + form_data + '''
                        <hr class="main_hr">
                        <button ''' + stat + ''' type="submit">''' + load_lang('add') + '''</button>
                    </form>
                    ''',
            menu = [[re.sub('^plus_', '', tools), load_lang('return')]]
        ))