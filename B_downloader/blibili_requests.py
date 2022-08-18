# B站专属请求模块
import requests,time
from cookies import cookies

def get_response(url):
    requests.adapters.DEFAULT_RETRIES = 5
    headers ={'origin':'https://www.bilibili.com','referer':'https://www.bilibili.com','user-agent':'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'}
    try:
        response  = requests.get(url=url,headers=headers,cookies=cookies,stream=True,timeout=20)
    except requests.exceptions.ConnectTimeout:
        print('无效链接，响应超时，请重新请求')
        time.sleep(3)
        exit(1)
    except:
        print('未知网络错误，请重新请求')
        exit(1)
    return response 
# 无效链接，响应超时，请重新请求
# Traceback (most recent call last):
#   File "urllib3/connection.py", line 144, in _new_conn
#   File "urllib3/util/connection.py", line 83, in create_connection
#   File "urllib3/util/connection.py", line 73, in create_connection
# socket.timeout: timed out

# During handling of the above exception, another exception occurred:

# Traceback (most recent call last):
#   File "urllib3/connectionpool.py", line 601, in urlopen
#   File "urllib3/connectionpool.py", line 346, in _make_request
#   File "urllib3/connectionpool.py", line 852, in _validate_conn
#   File "urllib3/connection.py", line 298, in connect
#   File "urllib3/connection.py", line 149, in _new_conn
# urllib3.exceptions.ConnectTimeoutError: (<urllib3.connection.VerifiedHTTPSConnection object at 0x7f3fa3b04f28>, 'Connection to xy27x8x181x228xy.mcdn.bilivideo.cn timed out. (connect timeout=20)')

# During handling of the above exception, another exception occurred:

# Traceback (most recent call last):
#   File "requests/adapters.py", line 440, in send
#   File "urllib3/connectionpool.py", line 639, in urlopen
#   File "urllib3/util/retry.py", line 398, in increment
# urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='xy27x8x181x228xy.mcdn.bilivideo.cn', port=4483): Max retries exceeded with url: /upgcxcode/26/35/486133526/486133526_nb2-1-30064.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1660653928&gen=playurlv2&os=mcdn&oi=453837852&trid=000087efac689e32407a8fcd1e4fa93c55eep&mid=470586328&platform=pc&upsig=0d4cb2ced0de2325ca9d0ba370c7220c&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&mcdnid=2002042&bvc=vod&nettype=0&orderid=0,3&agrr=1&bw=95285&logo=A0000002 (Caused by ConnectTimeoutError(<urllib3.connection.VerifiedHTTPSConnection object at 0x7f3fa3b04f28>, 'Connection to xy27x8x181x228xy.mcdn.bilivideo.cn timed out. (connect timeout=20)'))

# During handling of the above exception, another exception occurred:

# Traceback (most recent call last):
#   File "blibili_requests.py", line 9, in get_response
#   File "requests/api.py", line 72, in get
#   File "requests/api.py", line 58, in request
#   File "requests/sessions.py", line 520, in request
#   File "requests/sessions.py", line 630, in send
#   File "requests/adapters.py", line 496, in send
# requests.exceptions.ConnectTimeout: HTTPSConnectionPool(host='xy27x8x181x228xy.mcdn.bilivideo.cn', port=4483): Max retries exceeded with url: /upgcxcode/26/35/486133526/486133526_nb2-1-30064.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1660653928&gen=playurlv2&os=mcdn&oi=453837852&trid=000087efac689e32407a8fcd1e4fa93c55eep&mid=470586328&platform=pc&upsig=0d4cb2ced0de2325ca9d0ba370c7220c&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&mcdnid=2002042&bvc=vod&nettype=0&orderid=0,3&agrr=1&bw=95285&logo=A0000002 (Caused by ConnectTimeoutError(<urllib3.connection.VerifiedHTTPSConnection object at 0x7f3fa3b04f28>, 'Connection to xy27x8x181x228xy.mcdn.bilivideo.cn timed out. (connect timeout=20)'))

# During handling of the above exception, another exception occurred:

# Traceback (most recent call last):
#   File "main.py", line 6, in <module>
#   File "b_drama.py", line 79, in main
#   File "v_downloader.py", line 116, in chips
#   File "v_downloader.py", line 10, in chips_download
#   File "blibili_requests.py", line 13, in get_response
# NameError: name 'exit' is not defined
# [2593499] Failed to execute script 'main' due to unhandled exception!