from .tool.func import *
from . import main_error_404

def main_file_2(conn, data):
    curs = conn.cursor()

    if data == 'easter_egg.html':
        return easy_minify(flask.render_template(skin_check(),
            imp = ['easter_egg.html', wiki_set(), custom(), other2([0, 0])],
            data = open('./views/main_css/file/easter_egg.html', encoding='utf8').read(),
            menu = 0
        ))
    elif re.search(r'\.(txt|xml)$', data, flags = re.I):
        if data == 'robots.txt' and not os.path.exists('robots.txt'):
            return flask.Response('User-agent: *\nDisallow: /\nAllow: /$\nAllow: /w/', mimetype = 'text/plain')
        elif os.path.exists(data):
            if re.search(r'\.txt$', data, flags = re.I):
                return flask.send_from_directory('./', data, mimetype = 'text/plain')
            else:
                return flask.send_from_directory('./', data, mimetype = 'text/xml')

    return main_error_404.main_error_404_2(conn)