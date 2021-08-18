from scratchhh.scratchhh import Scratch
from gevent.pywsgi import WSGIServer
from flask import *
import datetime
import logging
import json
import os
import re

os.chdir(os.getcwd()+'\\application')
logging.basicConfig(filename='errors{}.log'.format(datetime.datetime.now().strftime('%m.%d.%y')), encoding='utf-8', level=logging.DEBUG)

app = Flask(__name__)

def run():
    @app.route('/')
    def home():
        return '{}'.format(open('./html/index.html', encoding='utf-8').read())

    @app.route('/projects/<query>')
    def project(query):
        search = json.loads(str(Scratch.getInfo(query)).replace("'", '"'))

        try:
            comments = Scratch.getProjComments(query, 3)
        except IndexError:
            comments = None

        rep = {'//views': str(search['stats']['views']), '//rem': str(search['stats']['remixes']), '//stars': str(search['stats']['favorites']), '//loves': str(search['stats']['loves']), '.id.': query, '//project-title': '{} by {}'.format(search['title'], search['author'])}
        if not search['remix'] == 'False':
                rep['//rmixstatus'] = 'Remix of {} by {}'.format(Scratch.getInfo(str(search['remix']))['title'], Scratch.getInfo(str(search['remix']))['author'])
        else:
                rep['//rmixstatus'] = ''
        if comments:
                rep['//comment1'] = '<i>{}</i>: {}<br><p style="font-size: xx-small">{}</p>'.format(comments[0][0], comments[0][1], comments[0][2])
                rep['//comment2'] = '<i>{}</i>: {}<br><p style="font-size: xx-small">{}</p>'.format(comments[1][0], comments[1][1], comments[1][2])
                rep['//comment3'] = '<i>{}</i>: {}<br><p style="font-size: xx-small">{}</p>'.format(comments[2][0], comments[2][1], comments[2][2])
        else:
                rep['//comment1'] = ''
                rep['//comment2'] = ''
                rep['//comment3'] = ''

        try: 
            rep = dict((re.escape(k), v) for k, v in rep.items())
            pattern = re.compile("|".join(rep.keys()))

            text = pattern.sub(lambda m: rep[re.escape(m.group(0))], open('./html/getproject.html', encoding='utf-8').read())

            return text
        except Exception as e:
            logging.error('{}; 404 page sent'.format(e))
            return open('./html/404.html', encoding='utf-8').read()

    @app.route('/projects/<query>/get', methods=['GET'])
    def get(query):
        try:
            Scratch.cloneProj(query, file='./projcache/project{}.sb3'.format(query))
            return send_file('./projcache/project{}.sb3'.format(query))
            
        except Exception as e:
            logging.error('{}; 404 page sent'.format(e))
            return open('./html/404.html', encoding='utf-8').read()

    server = WSGIServer(('0.0.0.0', 2000), app)
    server.serve_forever()
    