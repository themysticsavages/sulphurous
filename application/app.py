from scratchclient import ScratchSession, ScratchExceptions
from scratchhh.scratchhh import Scratch
from gevent.pywsgi import WSGIServer
from functools import update_wrapper
from datetime import timedelta
from dateutil import parser
from flask import *
import generator3
import requests
import pathlib
import filecmp
import zipfile
import random
import shutil
import base64
import json
import os
import re

app = Flask(__name__)
config = json.loads(open('./application/config.json').read())


def zipdir():
      with zipfile.ZipFile('./projcache/assets.zip', 'w') as zipObj:
            for folderName, subfolders, filenames in os.walk('./projcache/assets'):
                  for filename in filenames:
                        filePath = os.path.join(folderName, filename)
                        zipObj.write(filePath, os.path.basename(filePath))

class check:
  def checkbans(ip):
    if ip in config['ip_bans']:
      return True
    else:
      return None
  def checkpid(q):
    if q in config['pid_bl']:
      return True
    else:
      return None

def crossdomain(origin=None, methods=None, headers=None, max_age=21600, attach_to_all=True, automatic_options=True):
  if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
  if headers is not None and not headers:
        headers = ', '.join(x.upper() for x in headers)
  if not origin:
        origin = ', '.join(origin)
  if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

  def get_methods():
        if methods is not None:
              return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

  def decorator(f):
        def wrapped_function(*args, **kwargs):
              if automatic_options and request.method == 'OPTIONS':
                    resp = current_app.make_default_options_response()
              else:
                    resp = make_response(f(*args, **kwargs))
              if not attach_to_all and request.method != 'OPTIONS':
                    return resp

              h = resp.headers

              h['Access-Control-Allow-Origin'] = origin
              h['Access-Control-Allow-Methods'] = get_methods()
              h['Access-Control-Max-Age'] = str(max_age)
              if headers is not None:
                    h['Access-Control-Allow-Headers'] = headers
              return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
  return decorator

@app.url_value_preprocessor
def after(endpoint, r):
  if check.checkbans(request.remote_addr) == True:
    abort(403)
  try: os.remove('./projcache/assets.zip')
  except FileNotFoundError: pass

@app.get('/')
@crossdomain(origin='*')
def home():
    return open('./html/index.html', encoding='utf-8').read().replace('.coolstring.', random.choice(['has a few easter eggs', 'kinda mobile friendly', 'not dead!', 'with gist creation', 'bottom text', '^ click the logo! ^', '<a href="https://youtu.be/dQw4w9WgXcQ">you found waldo</a>']))

@app.get('/.git/')
def git():
    return redirect('https://github.com/themysticsavages/scratchhh.xyz')

@app.get('/500/')
def fivehundred():
    abort(500)

@app.get('/search/')
def search():
    args = request.args
    if not args.get('q'): return 'Search for something!!'

    return open('./html/search.html', encoding='utf-8').read().replace('.s.', args.get('q'))

@app.get('/projects/<query>/')
def project(query):
    if check.checkpid(query) == True: abort(500)
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

      if os.path.isdir('./projcache/{}'.format(query)):
        rep['<!--0'] = ''
        rep['0-->'] = ''

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

@app.get('/projects/<query>/get/')
def get(query):
    def download(url:str, file:str):
        r = requests.get(url, stream=True)

        if r.status_code == 200:
            with open(file, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            f.close()
    try:
        pathlib.Path('./projcache/{}'.format(query)).mkdir(parents=True, exist_ok=True)
        get_prev = False
        i = 0

        if os.path.exists('./projcache/{}/project{}-{}.sb3'.format(query, query, i)) == True:
              while os.path.exists('./projcache/{}/project{}-{}.sb3'.format(query, query, i)) == True:
                    if os.path.exists('./projcache/{}/project{}-{}.sb3'.format(query, query, i)) == False:
                          break
                    else:
                          i += 1
              download('https://projects.scratch.mit.edu/{}'.format(query), './projcache/{}/project{}-{}.sb3'.format(query, query, i))
              if filecmp.cmp('./projcache/{}/project{}-{}.sb3'.format(query, query, i), './projcache/{}/project{}-{}.sb3'.format(query, query, i - 1)) == True:
                    get_prev = './projcache/{}/project{}-{}.sb3'.format(query, query, i - 1)  
                    os.remove('./projcache/{}/project{}-{}.sb3'.format(query, query, i))
        elif os.path.exists('./projcache/{}/project{}-{}'.format(query, query, i)) == False:
              download('https://projects.scratch.mit.edu/{}'.format(query), './projcache/{}/project{}-{}.sb3'.format(query, query, i))

        if get_prev == False:
              return send_file('./projcache/{}/project{}-{}.sb3'.format(query, query, i))
        else:
             return send_file(get_prev)

    except Exception as e:
        print(e)
        return open('./html/500.html', encoding='utf-8').read()

@app.get('/projects/<query>/sprites/get/')
def spritesget(query):
      try: os.mkdir('./projcache/assets') 
      except FileExistsError: pass

      generator3.Generator(query).toBlocks('./projcache/assets/')
      os.remove('./projcache/assets/results.txt')
      
      zipdir()
      return send_file('./projcache/assets.zip')

@app.get('/projects/<query>/comments/get/')
@crossdomain(origin='*')
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

@app.get('/projects/<id>/embed/')
def embed(id):
  if Scratch.exists(id) == True:
    search = json.loads(requests.get('https://api.scratch.mit.edu/projects/'+id).text)
    rep = {'//views': str(search['stats']['views']), '//rem': str(search['stats']['remixes']), '//stars': str(search['stats']['favorites']), '//loves': str(search['stats']['loves']), '.id.': id, '//project-title': '{} by {}'.format(search['title'], search['author']['username']), '//sharedate': str(search['history']['shared']).split('T')[0].replace('-', '.')}

    null = None
    if not search['remix']['root'] == null:
        remix = json.loads(requests.get('https://api.scratch.mit.edu/projects/'+str(search['remix']['root'])).text)
        rep['//rmixstatus'] = 'Remix of {} by {}'.format(remix['title'], remix['author']['username'])
    else:
        rep['//rmixstatus'] = ''
    
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], open('./html/embed.html', encoding='utf-8').read())

    return text
  else:
    abort(404)
    
@app.get('/projects/<id>/embed-light/')
def embedlight(id):
  if Scratch.exists(id) == True:
    search = json.loads(requests.get('https://api.scratch.mit.edu/projects/'+id).text)
    rep = {'//views': str(search['stats']['views']), '//rem': str(search['stats']['remixes']), '//stars': str(search['stats']['favorites']), '//loves': str(search['stats']['loves']), '.id.': id, '//project-title': '{} by {}'.format(search['title'], search['author']['username']), '//sharedate': str(search['history']['shared']).split('T')[0].replace('-', '.')}

    null = None
    if not search['remix']['root'] == null:
        remix = json.loads(requests.get('https://api.scratch.mit.edu/projects/'+str(search['remix']['root'])).text)
        rep['//rmixstatus'] = 'Remix of {} by {}'.format(remix['title'], remix['author']['username'])
    else:
        rep['//rmixstatus'] = ''
    
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], open('./html/embed-light.html', encoding='utf-8').read())

    return text
  else:
    abort(404)

@app.get('/whyus/')
def us():
  return open('./html/whyus.html', encoding='utf-8').read()

@app.errorhandler(404)
def page_not_found(e):
  return open('./html/404.html', encoding='utf-8').read()

@app.errorhandler(403)
def forbidden(e):
  return open('./html/banned.html', encoding='utf-8').read().replace('.ip.', request.remote_addr)

@app.errorhandler(500)
def internal_error(e):
  return open('./html/500.html', encoding='utf-8').read()

@app.get('/api/archive/')
@crossdomain(origin='*')
def archiveapi():
  arc = { 'dirs': [] }
  for dir in os.listdir('./projcache'):
        arc['dirs'].append(dir)
  return arc

@app.get('/archive/docs/')
def archive_home():
      return open('./html/archivehelp.html', encoding='utf-8').read()

@app.get('/api/archive/<query>/')
@crossdomain(origin='*')
def archive_dir(query):
  if os.path.isdir('./projcache/{}'.format(query)) == True:
        arc = { 'projects': [] }
        for file in os.listdir('./projcache/{}'.format(query)):
              arc['projects'].append(str(file))
        return arc
  elif re.search('[@_!#$%^&*()<>?/\|}{~:]', query):
        return redirect('https://youtu.be/xvFZjo5PgG0', 307)
  else:
        abort(404)

@app.get('/api/archive/<query>/<file>/')
@crossdomain(origin='*')
def archive_file(query, file):
  if os.path.isdir('./projcache/{}'.format(query)) == True and pathlib.Path('./projcache/{}/{}'.format(query, file)).exists() == True:
        return send_file('./projcache/{}/{}'.format(query, file))
  elif re.search('[@_!#$%^&*()<>?/\|}{~:]', query):
        return redirect('https://youtu.be/xvFZjo5PgG0', 307)
  else:
        abort(404)

@app.get('/archive/')
def archive():
      return open('./html/archive.html').read()

@app.get('/archive/search/')
def archive_search():
      args = request.args
      if args.get('q') == '':
            abort(404)
      elif re.search('[@_!#$%^&*()<>?/\|}{~:]', args.get('q')):
        return redirect('https://youtu.be/xvFZjo5PgG0', 307)
      elif re.search('[a-zA-Z]', args.get('q')):
            abort(404)
      else:
            if os.path.isdir('./projcache/{}'.format(args.get('q'))) == True:
                  res = os.listdir('./projcache/{}'.format(args.get('q')))
                  html = open('./html/getarchproject.html', encoding='utf-8').read()
                  for file in res:
                    html = html+'<a href="/api/archive/{}/{}">{}</a> <br>'.format(args.get('q'), file, file)
                  return html.replace('//id', args.get('q'))+'</p> </body> </html>'
            else:
                  abort(404)

@app.get('/login/')
def login():
      return open('./html/login.html').read()

@app.get('/api/')
@crossdomain('*')
def api():
      return { 'ok?':'nokidding','why':'internal functions' } 

@app.get('/api/sendcomment/')
def sendcomment():
      args = request.args
      if args.get('user') == '' or args.get('pass') == '' or args.get('content') == '' or args.get('id') == '':
            abort(404)
      else:
            user = base64.b64decode(args.get('user').encode('ascii')).decode('ascii')
            passwd = base64.b64decode(args.get('pass').encode('ascii')).decode('ascii')

            cnt = args.get('content')
            pid = args.get('pid')

            ScratchSession(user, passwd).get_project(pid).post_comment(cnt)

      return redirect('/projects/{}'.format(pid))

@app.get('/api/checkuser/')
@crossdomain('*')
def checkuser():
  args = request.args
  return str(Scratch.exists(args.get('user')))

@app.get('/backpack/')
def backpack():
  return open('./html/backpack.html').read()

@app.get('/backpack/get/')
def getbackpack():
  args = request.args
  def download(url:str, file:str):
    r = requests.get(url, stream=True)

    if r.status_code == 200:
        with open(file, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        f.close()

  def get_user_backpack():
              user = base64.b64decode(args.get('user').encode('ascii')).decode('ascii')
              passwd = base64.b64decode(args.get('pass').encode('ascii')).decode('ascii')

              sess = ScratchSession(user, passwd)
              headers = {
                    "x-csrftoken": sess.csrf_token,
                    "X-Token": sess.token,
                    "x-requested-with": "XMLHttpRequest",
                    "Cookie": "scratchcsrftoken="
                    + sess.csrf_token
                    + ";scratchlanguage=en;scratchsessionsid="
                    + sess.session_id
                    + ";",
                    "referer": "https://scratch.mit.edu/users/" + user + "/",
              }
              req = requests.get('https://backpack.scratch.mit.edu/'+user+'/', headers=headers)
              return req.text

  if args.get('user') == '' or args.get('pass') == '':
        abort(404)
  else:
        try:
          os.mkdir('./projcache/assets')
        except FileExistsError:
          pass

        userb = json.loads(get_user_backpack())
        for cnt in userb:
              if '.zip' in cnt['body']: continue
              if '.json' in cnt['body']: continue

              download('https://assets.scratch.mit.edu/{}'.format(cnt['body']),'./projcache/assets/{}'.format(cnt['body']))
        zipdir()
        shutil.rmtree('./projcache/assets')
  return send_file('./projcache/assets.zip')

@app.get('/api/gists/get/')
def apigetgists():
  args = request.args
  fig = {'gists':[]}
  
  if args.get('l'):
    limit = args.get('l')
    gists = json.loads(open('./gists.json').read())

    if int(limit) > len(gists['gists']): abort(500)
    for i in range(int(limit)):
      fig['gists'].append(gists['gists'][0])

  res = jsonify(fig)
  res.headers.add('Access-Control-Allow-Origin', '*')
  return res

@app.get('/api/gists/all/')
def apiallgists():
  gists = json.loads(open('./gists.json').read())

  res = jsonify({'count':len(gists['gists']),'gists':gists['gists']})
  res.headers.add('Access-Control-Allow-Origin', '*')
  return res

@app.get('/api/gists/post/')
def apipostgists():
  args = request.args

  user = args.get('u')
  passwd = args.get('p')
  content = args.get('c')
  title = args.get('t')

  if user == None or passwd == None or content == None or title == None: abort(500)
  try:
        ScratchSession(user,passwd)
  except ScratchExceptions.InvalidCredentialsException:
        abort(500)
  
  gists = json.loads(open('./gists.json').read())
  gists['gists'].append({'user':user,'content':content,'id':random.randint(1,9999999),'title':title})
  
  open('./gists.json', 'w').write(
  str(gists).replace("'",'"')
  )

  return redirect('/gists/create/')

@app.get('/api/gists/getbyid/')
def apigetbyidgists():
      id = request.args.get('id')
      gists = json.loads(open('./gists.json').read())

      for gist in gists['gists']:
            if gist['id'] == int(id):
                  return gist

@app.get('/gists/')
def gists():
      return open('./html/gists.html', encoding='utf-8').read()

@app.get('/gists/<id>/')
def apirendergists(id):
      gists = json.loads(open('./gists.json').read())
      r = None

      for gist in gists['gists']:
            try:
                  if gist['id'] == int(id):
                        r = gist
            except ValueError:
                  abort(404)

      try:
            return open('./html/render.html').read().replace('//title', r['title']).replace('//author', r['user']).replace('//code', r['content'])
      except TypeError:
            abort(404)

@app.get('/gists/create/')
def gistcreate():
      return open('./html/creategist.html').read()

def run():
    server = WSGIServer((config['host'], config['port']), app)
    server.serve_forever()
