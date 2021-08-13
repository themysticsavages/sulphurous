from scratchhh.scratchhh import Scratch
from flask import *
import json
import os
import re

os.chdir(os.getcwd()+'\\okscratch')
app = Flask(__name__)

def run():
    @app.route('/')
    def home():
        return '{}'.format(open('./html/index.html', encoding='utf-8').read())

    @app.route('/search/<query>')
    def user(query):
        try:
            search = json.loads(str(Scratch.getInfo(query)).replace("'", '"'))
            return re.sub('//rem', str(search['stats']['remixes']), re.sub('.id.', query, '{}'
            .format(open('./html/getproject.html', encoding='utf-8').read()
            .replace('//project-title', '{} by {}'.format(search['title'], search['author']))
            .replace('//views', str(search['stats']['views'])))))
        except Exception as e:
            print(e)
            return open('./html/404.html', encoding='utf-8').read()

    if __name__ == 'okscratch.server':
        app.run(port=2000)