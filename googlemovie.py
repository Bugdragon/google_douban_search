# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, send_from_directory
import os
import redis
import json
import urllib.parse # python3
import requests
app = Flask(__name__)
r = redis.Redis(host='127.0.0.1')

proxies = {
    "http": "http://127.0.0.1:8087",
    "https": "http://127.0.0.1:8087",
}

# 谷歌url
api_url = 'https://www.googleapis.com/customsearch/v1'
# 豆瓣url
db_url = 'http://api.douban.com/v2/movie/search'

def get_search(start, query, proxy):
    #keys_count = r.llen('keys')
    #search_count = r.incr('google200search')
    #key = r.lindex('keys', search_coun t % keys_count)
    query = urllib.parse.quote(query.encode('utf-8')) # python3的quote
    # key需要自己申请
    url = api_url + '?key=AIzaSyD0RQ7mib89RHbdi4FjftXuBUMML03tSGs&cx=006049295558414440210:bttypk5pjn8' + '&q=' + query
    if int(start) > 0:
        url = url + '&start=' + str(start)
    if int(proxy) > 0:
        return requests.get(url, proxies=proxies, verify=False, timeout=2).text
    else:
        return requests.get(url, timeout=100).text

def get_moviesearch(start, query, proxy):
    #keys_count = r.llen('keys')
    #search_count = r.incr('google200search')
    #key = r.lindex('keys', search_coun t % keys_count)
    query = urllib.parse.quote(query.encode('utf-8')) # python3的quote
    url = db_url + '?tag=' + query
    if int(start) > 0:
        url = url + '&start=' + str(start)
    if int(proxy) > 0:
        return requests.get(url, proxies=proxies, verify=False, timeout=2).text
    else:
        return requests.get(url, timeout=100).text


@app.route('/static/<sfile>')
def static_file(sfile=None):
    return send_from_directory(os.path.join(app.root_path, 'static'), sfile)


@app.route('/status')
def status():
    count = request.args.get('c', '0')
    rcount = request.args.get('r', '0')
    queries = r.zrevrange('querys', 0, int(count), withscores=True)
    vos = []
    recently = r.lrange("recently", 0, rcount)
    for t in recently:
        vos.append((t.decode('utf-8'), '-'))
    for t in queries:
        vos.append((t[0].decode('utf-8'), int(t[1])))
    return render_template('status.html', queries=vos)


@app.route('/search')
def search():
    q = request.args.get('q', '')
    # save recently query words
    r.lpush("recently", q)
    if (r.llen("recently") > 200):
        r.rpop("recently")

    p = request.args.get('p', '0')
    words = q.split()
    words.sort()
    start = int(request.args.get('start', '0'))
    start = min(start, 90)
    key = '-'.join(words) + '-' + str(start)

    rvalue = r.get(key)

    j = None

    search = True
    if rvalue is not None:
        try:
            j = json.loads(rvalue)
            if 'items' in j:
                search = False
        except:
            j = None

    if search:
        rvalue = get_search(start, q, p)
        j = json.loads(rvalue)


    total_count = int(j['searchInformation']['totalResults'])
    start = start + 10
    cur_page = start / 10
    total_page = (total_count + 9) / 10
    total_page = min(total_page, 10)
    total_page = max(3, total_page)
    pre_page = max(cur_page - 1, 1)
    next_page = cur_page + 1 if cur_page < total_page else total_page
    first_page = 1 if cur_page <= 5 else cur_page - 5
    last_page = first_page + 9
    if (last_page > total_page):
        last_page = total_page
        first_page = max(1, total_page - 9)
    #r.zincrby('query', '-'.join(words))

    search_time = j['searchInformation']['formattedSearchTime']
    items = j['items'] if 'items' in j else []
    total_count = j['searchInformation'][
        'formattedTotalResults']

    return render_template('result.html', q=q, p=p,
                           search_time=search_time,
                           total_count=total_count,
                           items=items,
                           first_page=first_page,
                           last_page=last_page,
                           cur_page=cur_page,
                           pre_page=pre_page,
                           next_page=next_page)


@app.route('/moviesearch')
def moviesearch():
    q = request.args.get('q', '')
    # save recently query words
    r.lpush("recently", q)
    if (r.llen("recently") > 200):
        r.rpop("recently")

    p = request.args.get('p', '0')
    words = q.split()
    words.sort()
    start = int(request.args.get('start', '0'))
    start = min(start, 90)
    key = '-'.join(words) + '-' + str(start)

    rvalue = r.get(key)

    j = None

    search = True
    if rvalue is not None:
        try:
            j = json.loads(rvalue)
            if 'items' in j:
                search = False
        except:
            j = None

    if search:
        rvalue = get_moviesearch(start, q, p)
        j = json.loads(rvalue)


    total_count = int(j['count'])
    start = start + 10
    cur_page = start / 10
    total_page = (total_count + 9) / 10
    total_page = min(total_page, 10)
    total_page = max(3, total_page)
    pre_page = max(cur_page - 1, 1)
    next_page = cur_page + 1 if cur_page < total_page else total_page
    first_page = 1 if cur_page <= 5 else cur_page - 5
    last_page = first_page + 9
    if (last_page > total_page):
        last_page = total_page
        first_page = max(1, total_page - 9)
    #r.zincrby('query', '-'.join(words))

    
    subjects = j['subjects'] if 'subjects' in j else []
    total_count = j['count']

    return render_template('movieresult.html', q=q, p=p,
                           total_count=total_count,
                           subjects=subjects,
                           first_page=first_page,
                           last_page=last_page,
                           cur_page=cur_page,
                           pre_page=pre_page,
                           next_page=next_page)


@app.route('/')
def index():
    return render_template('index.html', use_proxy=0)

if __name__ == '__main__':
    app.run(debug=True)
