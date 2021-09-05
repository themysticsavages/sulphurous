from scratchhh.scratchhh import Scratch
from gevent.pywsgi import WSGIServer
from dateutil import parser
from flask import *
import logging
import requests
import json
import os
import re

app = Flask(__name__)

def run():
    @app.route('/')
    def home():
        return '{}'.format(open('./html/index.html', encoding='utf-8').read())

    @app.route('/projects/<query>/')
    def project(query):
        if Scratch.exists(query) == True and re.match('^[0-9]*$', query):
          search = Scratch.getInfo(query)
          try:
            comments = Scratch.getProjComments(query, 3)
          except IndexError:
            comments = None
          print(comments)

          rep = {'//views': str(search['stats']['views']), '//rem': str(search['stats']['remixes']), '//stars': str(search['stats']['favorites']), '//loves': str(search['stats']['loves']), '.id.': query, '//project-title': '{} by {}'.format(search['title'], search['author']), '//sharedate': str(search['share']).split('T')[0].replace('-', '.')}
          if not search['remix'] == 'False':
            rep['//rmixstatus'] = 'Remix of {} by {}'.format(Scratch.getInfo(str(search['remix']))['title'], Scratch.getInfo(str(search['remix']))['author'])
          else:
            rep['//rmixstatus'] = ''
          
          if not search['desc'] == '':
            rep['//description'] = search['desc']
            rep['<!--1'] = ''
            rep['1-->'] = ''
      
          if comments:
            try:
              if comments[0]:
                  try:
                        parser.parse(comments[0][2])
                        rep['//comment1'] = '<i>{}</i>: {}<br><p style="font-size: xx-small">{}</p>'.format(comments[0][0], comments[0][1], comments[0][2])
                  except parser.ParserError:
                        rep['//comment1'] = '<i>{}</i>: {}, {}<br><p style="font-size: xx-small">{}</p>'.format(comments[0][0], comments[0][1], comments[0][2], comments[0][3])
            except IndexError:
                  rep['//comment1'] = ''
            try:
              if comments[1]:
                  try:
                        parser.parse(comments[1][2])
                        rep['//comment2'] = '<i>{}</i>: {}<br><p style="font-size: xx-small">{}</p>'.format(comments[1][0], comments[1][1], comments[1][2])
                  except parser.ParserError:
                        rep['//comment2'] = '<i>{}</i>: {}, {}<br><p style="font-size: xx-small">{}</p>'.format(comments[1][0], comments[1][1], comments[1][2], comments[1][3])
            except IndexError:
                  rep['//comment2'] = ''
            try:
              if comments[2]:
                  try:
                        parser.parse(comments[2][2])
                        rep['//comment3'] = '<i>{}</i>: {}<br><p style="font-size: xx-small">{}</p>'.format(comments[2][0], comments[2][1], comments[2][2])
                  except parser.ParserError:
                        rep['//comment3'] = '<i>{}</i>: {}, {}<br><p style="font-size: xx-small">{}</p>'.format(comments[2][0], comments[2][1], comments[2][2], comments[2][3])
            except IndexError:
                  rep['//comment3'] = ''
          else:
            rep['//comment1'] = '<sub>(None)</sub>'
            rep['//comment2'] = ''
            rep['//comment3'] = ''
          
          rep = dict((re.escape(k), v) for k, v in rep.items())
          pattern = re.compile("|".join(rep.keys()))
          text = pattern.sub(lambda m: rep[re.escape(m.group(0))], open('./html/getproject.html', encoding='utf-8').read())

          return text
        else:
          print('Project did not exist or ID invalid; Returning 404 page')
          return open('./html/404.html', encoding='utf-8').read()

    @app.route('/projects/<query>/get/', methods=['GET'])
    def get(query):
        try:
            Scratch.cloneProj(query, file='./projcache/project{}.sb3'.format(query))
            return send_file('./projcache/project{}.sb3'.format(query))
            
        except Exception as e:
            print(e)
            return open('./html/404.html', encoding='utf-8').read()

    @app.route('/projects/<query>/comments/get/', methods=['GET'])
    def commentsget(query):
          try:
            comments = Scratch.getProjComments(query, 3)
          except IndexError:
            comments = None
          print(comments)

          rep = {'.id.': query}
      
          if comments:
            try:
              if comments[0]:
                  try:
                        parser.parse(comments[0][2])
                        rep['//comment1'] = '<i>{}</i>: {}<br><p style="font-size: xx-small">{}</p>'.format(comments[0][0], comments[0][1], comments[0][2])
                  except parser.ParserError:
                        rep['//comment1'] = '<i>{}</i>: {}, {}<br><p style="font-size: xx-small">{}</p>'.format(comments[0][0], comments[0][1], comments[0][2], comments[0][3])
            except IndexError:
                  rep['//comment1'] = ''
            try:
              if comments[1]:
                  try:
                        parser.parse(comments[1][2])
                        rep['//comment2'] = '<i>{}</i>: {}<br><p style="font-size: xx-small">{}</p>'.format(comments[1][0], comments[1][1], comments[1][2])
                  except parser.ParserError:
                        rep['//comment2'] = '<i>{}</i>: {}, {}<br><p style="font-size: xx-small">{}</p>'.format(comments[1][0], comments[1][1], comments[1][2], comments[1][3])
            except IndexError:
                  rep['//comment2'] = ''
            try:
              if comments[2]:
                  try:
                        parser.parse(comments[2][2])
                        rep['//comment3'] = '<i>{}</i>: {}<br><p style="font-size: xx-small">{}</p>'.format(comments[2][0], comments[2][1], comments[2][2])
                  except parser.ParserError:
                        rep['//comment3'] = '<i>{}</i>: {}, {}<br><p style="font-size: xx-small">{}</p>'.format(comments[2][0], comments[2][1], comments[2][2], comments[2][3])
            except IndexError:
                  rep['//comment3'] = ''

          rep = dict((re.escape(k), v) for k, v in rep.items())
          pattern = re.compile("|".join(rep.keys()))
          text = pattern.sub(lambda m: rep[re.escape(m.group(0))], open('./html/rawcomments.html', encoding='utf-8').read())

          return text
    @app.route('/projects/<query>/embed/')
    def embed(query):
            try:
                  search = json.loads(str(Scratch.getInfo(query)).replace("'", '"'))
            except KeyError:
                  return open('./html/404.html', encoding='utf-8').read()
            rep = {'//views': str(search['stats']['views']), '//rem': str(search['stats']['remixes']), '//stars': str(search['stats']['favorites']), '//loves': str(search['stats']['loves']), '.id.': query, '//project-title': '{} by {}'.format(search['title'], search['author'])}
            if not search['remix'] == 'False':
                  rep['//rmixstatus'] = 'Remix of {} by {}'.format(Scratch.getInfo(str(search['remix']))['title'], Scratch.getInfo(str(search['remix']))['author'])
            else:
                  rep['//rmixstatus'] = ''

            rep = dict((re.escape(k), v) for k, v in rep.items())
            pattern = re.compile("|".join(rep.keys()))
            text = pattern.sub(lambda m: rep[re.escape(m.group(0))], open('./html/embed.html', encoding='utf-8').read())

            return text
    @app.route('/projects/<query>/embed-light/')
    def embed_light(query):
            try:
                  search = json.loads(str(Scratch.getInfo(query)).replace("'", '"'))
            except KeyError:
                  return open('./html/404.html', encoding='utf-8').read()
            rep = {'//views': str(search['stats']['views']), '//rem': str(search['stats']['remixes']), '//stars': str(search['stats']['favorites']), '//loves': str(search['stats']['loves']), '.id.': query, '//project-title': '{} by {}'.format(search['title'], search['author'])}
            if not search['remix'] == 'False':
                  rep['//rmixstatus'] = 'Remix of {} by {}'.format(Scratch.getInfo(str(search['remix']))['title'], Scratch.getInfo(str(search['remix']))['author'])
            else:
                  rep['//rmixstatus'] = ''

            rep = dict((re.escape(k), v) for k, v in rep.items())
            pattern = re.compile("|".join(rep.keys()))
            text = pattern.sub(lambda m: rep[re.escape(m.group(0))], open('./html/embed-light.html', encoding='utf-8').read())

            return text
    @app.route('/whyus')
    def us():
      return open('./html/whyus.html', encoding='utf-8').read()
    @app.errorhandler(404)
    def page_not_found(e):
      return open('./html/404.html', encoding='utf-8').read()

    server = WSGIServer(('0.0.0.0', 2000), app)
    server.serve_forever()