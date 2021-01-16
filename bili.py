import urllib.request as librequest
import urllib.error as liberror
import urllib.parse as libparse
import time
import random
import json

def main():
    print('输入动态id：')
    dynamic_id = input()
    backurl_str = UrlGet("https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id=" + dynamic_id)
    json_load = json.loads(backurl_str)
    oid = json_load['data']['card']['desc']['rid']

    replylist = []
    for page in range(1,10000):
        backurl_str = UrlGet("https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn=" + str(page) +"&type=11&sort=0&oid=" + str(oid))
        json_load = json.loads(backurl_str)
        if json_load['data']['replies'] is None:
            break
        for reply in json_load['data']['replies']:
            replylist.append(['https://space.bilibili.com/' + reply['member']['mid'],reply['member']['uname'],reply['content']['message']])
        random.shuffle(replylist)
        print('第'+ str(page) + '页获取完毕')
    
    random.seed(int(round(time.time() * 1000)))
    winer = replylist[random.randint(0,len(replylist)-1)]

    print('中奖人为：')
    print('id： ' + winer[1])
    print('空间链接：' + winer[0])
    print('评论内容： ' + winer[2])
    
def UrlGet(Url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36",
        "Cookie": ""
    }
    request = librequest.Request(url=Url, headers=head)
    html = ""
    try:
        response = librequest.urlopen(request)
        html = response.read()
        try:
            html = html.decode("gbk")
        except UnicodeDecodeError as e:
            try:
                html = html.decode("utf8")
            except UnicodeDecodeError as e:
                html = html.decode("gb18030")
        return html
    except liberror.URLError as e:
        if hasattr(e, "code"):
            print(e.errno)
        if hasattr(e, "reason"):
            print(e.reason)
        return 'error'

if __name__ == "__main__":
    main()