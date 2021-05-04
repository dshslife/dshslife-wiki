from .tool.func import *

def main_manager_2(conn, num, r_ver):
    curs = conn.cursor()

    title_list = {
        0 : [load_lang('document_name'), 'acl', load_lang('acl')],
        1 : [0, 'check', load_lang('check')],
        2 : [load_lang('file_name'), 'plus_file_filter', load_lang('file_filter_add')],
        3 : [0, 'admin', load_lang('authorize')],
        4 : [0, 'record', load_lang('edit_record')],
        5 : [0, 'topic_record', load_lang('discussion_record')],
        6 : [load_lang('name'), 'admin_plus', load_lang('add_admin_group')],
        7 : [load_lang('name'), 'plus_edit_filter', load_lang('edit_filter_add')],
        8 : [load_lang('document_name'), 'search', load_lang('search')],
        9 : [0, 'block_user', load_lang('blocked_user')],
        10 : [0, 'block_admin', load_lang('blocked_admin')],
        11 : [load_lang('document_name'), 'watch_list', load_lang('add_watchlist')],
        12 : [load_lang('compare_target'), 'check', load_lang('compare_target')],
        13 : [load_lang('document_name'), 'edit', load_lang('load')],
        14 : [load_lang('document_name'), 'star_doc', load_lang('add_star_doc')],
        15 : [load_lang('name_or_ip_or_regex'), 'ban', load_lang('release')]
    }

    if num == 1:
        return easy_minify(flask.render_template(skin_check(),
            imp = [load_lang('admin_tool'), wiki_set(), custom(), other2([0, 0])],
            data = '''
                <h2>''' + load_lang('admin') + '''</h2>
                <ul class="inside_ul">
                    <li><a href="/manager/2">''' + load_lang('acl_change') + '''</a></li>
                    <li><a href="/manager/3">''' + load_lang('check_user') + '''</a></li>
                    <li><a href="/ban">''' + load_lang('ban') + '''</a></li>
                    <li><a href="/manager/17">''' + load_lang('release') + '''</a></li>
                    <li><a href="/manager/5">''' + load_lang('authorize') + '''</a></li>
                </ul>
                <br>
                <h2>''' + load_lang('owner') + '''</h2>
                <ul class="inside_ul">
                    <li><a href="/give_log">''' + load_lang('admin_group_list') + '''</a></li>
                    <li><a href="/many_delete">''' + load_lang('many_delete') + '''</a></li>
                    <li><a href="/applications">''' + load_lang('application_list') + '''</a></li>
                    <li><a href="/api/sitemap.xml">''' + load_lang('get_sitemap') + '''</a></li>
                    <li><a href="/register">''' + load_lang('add_user') + '''</a></li>
                    <li><a href="/setting">''' + load_lang('setting') + '''</a></li>
                </ul>
                <h3>''' + load_lang('filter') + '''</h3>
                <ul class="inside_ul">
                    <li><a href="/edit_filter">''' + load_lang('edit_filter_list') + '''</a></li>
                    <li><a href="/inter_wiki">''' + load_lang('interwiki_list') + '''</a></li>
                    <li><a href="/edit_top">''' + load_lang('edit_tool_list') + '''</a></li>
                    <li><a href="/image_license">''' + load_lang('image_license_list') + '''</a></li>
                    <li><a href="/email_filter">''' + load_lang('email_filter_list') + '''</a></li>
                    <li><a href="/name_filter">''' + load_lang('id_filter_list') + '''</a></li>
                    <li><a href="/file_filter">''' + load_lang('file_filter_list') + '''</a></li>
                    <li><a href="/extension_filter">''' + load_lang('extension_filter_list') + '''</a></li>
                </ul>
                <br>
                <h2>''' + load_lang('server') + '''</h2>
                <ul class="inside_ul">
                    <li><a href="/restart">''' + load_lang('wiki_restart') + '''</a></li>
                    <li><a href="/update">''' + load_lang('update') + '''</a></li>
                </ul>
                <br>
                <h2>''' + load_lang('version') + '''</h2>
                <ul class="inside_ul">
                    <li>
                        <a href="/api/skin_info?all=true">''' + load_lang('skin_info') + '''</a>
                        <span id="need_skin_update"></span>
                    </li>
                    <li>''' + load_lang('version') + ' : ' + r_ver + '''</li>
                    <li id="ver_send" style="display: none;">''' + load_lang('lastest') + ''' : </li>
                </ul>
                <script>load_ver(); do_skin_ver_check();</script>
            ''',
            menu = [['other', load_lang('return')]]
        ))
    elif not num - 1 > len(title_list):
        if flask.request.method == 'POST':
            if flask.request.args.get('plus', None):
                return redirect(
                    '/' + title_list[(num - 2)][1] + '/' + url_pas(flask.request.args.get('plus', 'test')) + '?plus=' + flask.request.form.get('name', 'test')
                )
            elif flask.request.form.get('regex', None):
                return redirect('/' + title_list[(num - 2)][1] + '/' + url_pas(flask.request.form.get('name', 'test')) + '?type=regex')
            else:
                return redirect('/' + title_list[(num - 2)][1] + '/' + url_pas(flask.request.form.get('name', 'test')))
        else:
            if title_list[(num - 2)][0] == 0:
                placeholder = load_lang('user_name')
            else:
                placeholder = title_list[(num - 2)][0]

            plus = ''
            if num - 2 == 15:
                plus = '<input type="checkbox" name="regex"> ' + load_lang('regex') + '<hr class="main_hr">'

            return easy_minify(flask.render_template(skin_check(),
                imp = [title_list[(num - 2)][2], wiki_set(), custom(), other2([0, 0])],
                data = '''
                    <form method="post">
                        <input placeholder="''' + placeholder + '''" name="name" type="text">
                        <hr class=\"main_hr\">
                        ''' + plus + '''
                        <button type="submit">''' + load_lang('go') + '''</button>
                    </form>
                ''',
                menu = [['manager', load_lang('return')]]
            ))
    else:
        return redirect()