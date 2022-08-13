# -*- coding: UTF-8 -*-
import json,os,re,requests,subprocess,time
from urllib.parse import quote
from cookies import cookies

# 网站请求
def get_response(url):
    headers = {
        'origin':'https://www.bilibili.com',
        'referer':'https://www.bilibili.com',
        'user-agent':'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'
    }
    response = requests.get(url=url,headers=headers,cookies=cookies)
    return response

# 获取追剧列表
def series_list(vmid):
    # vmid = re.findall(r"\d+\.?\d*",url)[0] 
    millis = int(round(time.time() * 1000))
    url = f'https://api.bilibili.com/x/space/bangumi/follow/list?type=1&follow_status=0&pn=1&ps=30&vmid={vmid}&ts={millis}' #获取50个剧集信息
    print(url)
    series_list_info = get_response(url).json()['data']['list']
    info = []
    for single in series_list_info:
        media_id = single['media_id']
        id_url = f'https://api.bilibili.com/pgc/review/user?media_id={media_id}'
        ep_id = get_response(id_url).json()['result']['media']['new_ep']['id']
        title = single['title'] + '--' + single['season_title']
        sinfo = f'{{\"name\":\"{title}",\"media_id\":\"{media_id}\",\"ep_id\":\"{ep_id}\"}}'
        sinfo = json.loads(sinfo)
        info.append(sinfo)
    return info

# 获取所选剧集信息
def seasons_info(vmid):
    res = series_list(vmid)
    a = 0
    for list_info in res:
        a=a+1
        msg = str(a) + '. ' +list_info['name']
        print(msg)
    chooise = int(input("输入编号："))-1
    ep_id = res[chooise]['ep_id']
    url = f'https://api.bilibili.com/pgc/view/web/season?ep_id={ep_id}'
    vs_info = get_response(url).json()['result']['episodes']
    urls = []
    for v_info in vs_info:
        aid = v_info['aid']
        cid = v_info['cid']
        v_title = v_info['share_copy']
        singel_url = f'https://api.bilibili.com/pgc/player/web/playurl?avid={aid}&cid={cid}&fnver=0&fnval=4048&fourk=1&ep_id={ep_id}'
        singel_url = f'{{\"v_title\":\"{v_title}\",\"singel_url\":\"{singel_url}\"}}'
        singel_url = json.loads(singel_url)
        urls.append(singel_url)
    return urls

# 下载视频和音频
def download(url,title):
    # print(url)#
    v_a_url = get_response(url).json()
    # print(v_a_url) #{'code': -10403, 'message': '大会员专享限制'}
    v_url = v_a_url['result']['dash']['video'][0]['baseUrl']
    a_url = v_a_url['result']['dash']['audio'][0]['baseUrl']

    print(f'正在下载视频：{title}')
    video_content = get_response(v_url).content
    with open(title + '.mp4',mode='wb') as f:
        f.write(video_content)
    
    print('开始下载音频...')
    audio_content = get_response(a_url).content
    with open(title + '.wav',mode='wb') as f:
        f.write(audio_content)    
    
    print(f'{title} 下载完成！\n 开始合并文件...')
    cmd = f'ffmpeg -i {title}.mp4 -i {title}.wav -c:v copy -c:a aac -strict experimental {title}.flv'
    subprocess.call(cmd,shell=True)
    os.remove(title+'.mp4')
    os.remove(title+'.wav')
    print(f'{title}--完成')

# 检测cookie是否失效
def check_cookie():
    check_url = f'https://account.bilibili.com/site/getCoin'
    check_result = get_response(check_url).json()
    if check_result['code'] == 0:
        coin_num = check_result['data']['money']
        print(f'Cookie有效，目前硬币为{coin_num}')
    else:
        print('请重新获取Cookie!!')
        cookie = input('输入你获取到的Cookie:')
        # cookie = quote(cookie,'utf-8')
        with open('cookie','w')as f:
            f.write(cookie)
            f.close()
        print('再次运行本程序！')
        exit()

# 启动
if __name__ == "__main__":
    spece_url = input(f'输入你主页的地址：')
    vmid = re.findall(r"\d+\.?\d*",spece_url)[0]
    print(vmid)
    # cookie = open('cookie').read()
    cookie = cookies
    # print(cookie)
    check_cookie()

    urls_json = seasons_info(vmid)
    for urls in urls_json:
        url = urls['singel_url']
        title = urls['v_title']
        title = str(title).replace(' ','_')
        download(url,title)
        print('下一个...')
    print('全部下载完成！')