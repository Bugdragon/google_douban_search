import requests
import json
import codecs
file = codecs.open('movie.json', 'w',encoding='utf-8')
#API
url = 'http://api.douban.com/v2/movie/search'
# 参数列表
start=5
count=25
tag="复仇者联盟"
r = requests.get(url, params={'tag': tag})
r.encoding='UTF_8'
content=r.json()
file.write(json.dumps(content,ensure_ascii=False))