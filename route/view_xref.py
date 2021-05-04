from .tool.func import *

def view_xref_2(conn, name):
    curs = conn.cursor()

    if acl_check(name, 'render') == 1:
        return re_error('/ban')

    num = int(number_check(flask.request.args.get('num', '1')))
    if num * 50 > 0:
        sql_num = num * 50 - 50
    else:
        sql_num = 0

    if flask.request.args.get('change', '1') == '1':
        div = '<a href="?change=2">(' + load_lang('link_in_this') + ')</a><hr class="main_hr">'
    else:
        div = '<a href="?change=1">(' + load_lang('normal') + ')</a><hr class="main_hr">'

    div += '<ul class="inside_ul">'

    if flask.request.args.get('change', '1') == '1':
        curs.execute(db_change("" + \
            "select distinct link, type from back " + \
            "where title = ? and not type = 'cat' and not type = 'no' and not type = 'nothing'" + \
            "order by link asc limit ?, 50" + \
        ""), [
            name,
            sql_num
        ])
    else:
        curs.execute(db_change("" + \
            "select distinct title, type from back " + \
            "where link = ? and not type = 'cat' and not type = 'no' and not type = 'nothing'" + \
            "order by link asc limit ?, 50" + \
        ""), [
            name,
            sql_num
        ])

    data_list = curs.fetchall()
    for data in data_list:
        div += '<li><a href="/w/' + url_pas(data[0]) + '">' + data[0] + '</a>'

        if data[1]:
            div += ' (' + data[1] + ')'

        curs.execute(db_change("select title from back where title = ? and type = 'include'"), [data[0]])
        db_data = curs.fetchall()
        if db_data:
            div += ' <a id="inside" href="/xref/' + url_pas(data[0]) + '">(' + load_lang('backlink') + ')</a>'

        div += '</li>'

    div += '</ul>' + next_fix('/xref/' + url_pas(name) + '?num=', num, data_list)

    return easy_minify(flask.render_template(skin_check(),
        imp = [name, wiki_set(), custom(), other2(['(' + load_lang('backlink') + ')', 0])],
        data = div,
        menu = [['w/' + url_pas(name), load_lang('return')], ['backlink_reset/' + url_pas(name), load_lang('reset_backlink')]]
    ))