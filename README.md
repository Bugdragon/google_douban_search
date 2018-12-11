# google_douban_search
+ 基于google custom search api的google搜索镜像
+ 基于豆瓣 api的简单搜索展示

### 安装指南
1. flask, redis, requests
2. google custom search api key
3. python googlemovie.py
4. http://127.0.0.1:5000/

##### douban.py
基于标签的豆瓣搜索，获取movie.json，方便解析。

##### google custom search api url
https://www.googleapis.com/customsearch/v1?key=INSERT_YOUR_API_KEY&cx=017576662512468239146:omuauf_lfve&q=lectures

##### douban api url
http://api.douban.com/v2/movie/search?tag=tag

### 网站
+ [custom search](https://developers.google.com/custom-search/)
+ [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/)
+ [idataapi](http://www.idataapi.cn/)
